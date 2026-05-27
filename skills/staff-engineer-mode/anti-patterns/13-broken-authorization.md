# RF-25: Broken Authorization

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-25

## Detection

A handler that fetches a resource by ID with no ownership/role check, or — worse — an authorization check that exists on one transport path (REST) but not another (gRPC, internal RPC, message consumer) that resolves to the same data. Grep for handler functions whose body goes straight from `vars["id"]` to `repo.Get(id)` with no `if user.Can(...)` between them. Code review red flag: two endpoints serving the same entity where only one mentions the requesting user.

## Smell

```go
package invoices

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)

type Handler struct {
	repo Repository
	auth AuthService
}

// REST: properly guarded
func (h *Handler) GetInvoiceREST(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	userID := r.Context().Value("userID").(string)

	inv, err := h.repo.Get(r.Context(), id)
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	if !h.auth.CanRead(userID, inv) {
		http.Error(w, "forbidden", http.StatusForbidden)
		return
	}
	_ = json.NewEncoder(w).Encode(inv)
}

// gRPC: added later for the mobile app, check forgotten
func (h *Handler) GetInvoice(ctx context.Context, req *pb.GetInvoiceRequest) (*pb.Invoice, error) {
	inv, err := h.repo.Get(ctx, req.GetId())
	if err != nil {
		return nil, status.Error(codes.NotFound, "not found")
	}
	return toProto(inv), nil
}
```

## Why this fails in production

The gRPC endpoint is now a fully open invoice-by-ID API: any authenticated user — including a free-tier signup from yesterday — can iterate sequential or UUID-guessed IDs and exfiltrate every customer's billing history, line items, and PII. This is OWASP's number-one ranked risk for a reason: scattering authorization across transport layers guarantees one of them eventually gets added without the check, and the gap is invisible to any test that only exercises the REST surface. Real-world examples (Facebook 2018, USPS 2018, Peloton 2021) all share this exact shape: a parallel API path that bypassed the web's enforced check. Discovery typically comes from a security researcher, not your monitoring.

## Fix

```go
package invoices

import (
	"context"
	"errors"
)

var ErrForbidden = errors.New("forbidden")

// Default-deny at the data-access layer: every read requires the actor.
// Higher layers (REST, gRPC, workers) can no longer forget the check —
// they cannot fetch an invoice without naming who is asking.
func (r *invoiceRepo) GetForActor(ctx context.Context, id, actorID string) (*Invoice, error) {
	inv, err := r.getByID(ctx, id)
	if err != nil {
		return nil, err
	}
	if !r.acl.CanRead(ctx, actorID, inv) {
		return nil, ErrForbidden // indistinguishable from not-found at the API edge
	}
	return inv, nil
}

func (h *Handler) GetInvoiceREST(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("userID").(string)
	inv, err := h.repo.GetForActor(r.Context(), mux.Vars(r)["id"], userID)
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	_ = json.NewEncoder(w).Encode(inv)
}

func (h *Handler) GetInvoice(ctx context.Context, req *pb.GetInvoiceRequest) (*pb.Invoice, error) {
	userID := actorFromContext(ctx)
	inv, err := h.repo.GetForActor(ctx, req.GetId(), userID)
	if err != nil {
		return nil, status.Error(codes.NotFound, "not found")
	}
	return toProto(inv), nil
}
```

## Reasoning

Authorization is a cross-cutting concern that must live at the layer no caller can bypass — typically the data-access boundary, not the transport layer. Scattering checks across REST/gRPC/CLI/worker handlers violates orthogonality: a behavior that should be one decision becomes N decisions, and N-1 of them eventually drift.

## Citation

- OWASP Top 10 (2021), A01:2021 — Broken Access Control. Ranked #1; appears in 94% of tested applications.
- *The Pragmatic Programmer*, Hunt & Thomas (20th Anniversary ed., 2019), Topic 10 "Orthogonality" — eliminate effects between unrelated things; one change, one place.

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/pragmatic-programmer.md
