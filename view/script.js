const API_BASE_URL = "http://localhost:8000";
const currencyBRL = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});
const integerBR = new Intl.NumberFormat("pt-BR");
const dateBR = new Intl.DateTimeFormat("pt-BR");

const state = {
  parts: [],
  sales: [],
  editingPartSku: null,
  editingSaleId: null,
};
const elements = {
  revenue: document.getElementById("revenue-content"),
  categories: document.getElementById("category-content"),
  count: document.getElementById("stagnant-count"),
  inventory: document.getElementById("inventory-content"),
  error: document.getElementById("global-error"),
  status: document.getElementById("status-area"),
  lastUpdate: document.getElementById("last-update"),
  refresh: document.getElementById("refresh-button"),
  partsTable: document.getElementById("parts-table"),
  salesTable: document.getElementById("sales-table"),
  salesCount: document.getElementById("sales-count"),
  insightsSummary: document.getElementById("insights-summary"),
  marginContent: document.getElementById("margin-content"),
  filterStart: document.getElementById("filter-start"),
  filterEnd: document.getElementById("filter-end"),
  filterStore: document.getElementById("filter-store"),
  filterCategory: document.getElementById("filter-category"),
  partForm: document.getElementById("part-form"),
  partFormTitle: document.getElementById("part-form-title"),
  saleForm: document.getElementById("sale-form"),
  saleEditor: document.getElementById("sale-editor"),
};

function escapeHTML(value) {
  return String(value ?? "").replace(
    /[&<>'"]/g,
    (character) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[
        character
      ],
  );
}

function setLoading(isLoading) {
  elements.refresh.disabled = isLoading;
  elements.refresh.innerHTML = isLoading
    ? '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>Carregando...'
    : '<i class="bi bi-arrow-clockwise me-2" aria-hidden="true"></i>Atualizar dados';
}

async function requestJSON(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(
      body.detail || `API respondeu com status ${response.status}`,
    );
  }
  return response.status === 204 ? null : response.json();
}

function renderCategories(categories) {
  const entries = categories
    .map(({ categoria, valor }) => [categoria, valor])
    .sort(([, first], [, second]) => second - first);
  if (!entries.length) {
    elements.categories.innerHTML =
      '<p class="empty-state mb-0">Nenhuma categoria disponível.</p>';
    return;
  }
  const maximum = Math.max(...entries.map(([, amount]) => amount), 1);
  elements.categories.innerHTML = entries
    .map(
      ([category, amount]) =>
        `<div class="ranking-row"><div class="ranking-label"><span>${escapeHTML(category)}</span><span>${currencyBRL.format(amount)}</span></div><div class="bar-track" role="progressbar" aria-label="${escapeHTML(category)}" aria-valuenow="${amount}" aria-valuemin="0" aria-valuemax="${maximum}"><div class="bar-fill" style="width: ${(amount / maximum) * 100}%"></div></div></div>`,
    )
    .join("");
}

function renderInventory(items) {
  if (!items.length) {
    elements.inventory.innerHTML =
      '<p class="empty-state p-4 mb-0">Nenhuma peça parada encontrada.</p>';
    return;
  }
  elements.inventory.innerHTML = `<table class="table table-hover mb-0"><caption class="visually-hidden">Peças nunca vendidas e seus estoques</caption><thead><tr><th>SKU</th><th>Nome da peça</th><th class="text-end">Estoque</th></tr></thead><tbody>${items.map((item) => `<tr><td class="sku">${escapeHTML(item.sku)}</td><td>${escapeHTML(item.nome_peca)}</td><td class="text-end fw-bold">${integerBR.format(item.estoque_atual)}</td></tr>`).join("")}</tbody></table>`;
}

function renderDashboard(revenue, categories, inventory) {
  elements.revenue.innerHTML = `<div class="metric-value">${currencyBRL.format(revenue.faturamento_total)}</div><p class="metric-caption mt-2 mb-0">Consolidado das vendas concluídas</p>`;
  elements.count.innerHTML = `<div class="metric-value">${integerBR.format(inventory.quantidade_total)}</div>`;
  renderCategories(categories.categorias);
  renderInventory(inventory.pecas);
  elements.lastUpdate.textContent = `Atualizado em ${dateBR.format(new Date())}`;
}

function renderParts() {
  elements.partsTable.innerHTML = state.parts.length
    ? state.parts
        .map(
          (part) =>
            `<tr><td class="sku">${escapeHTML(part.sku)}</td><td>${escapeHTML(part.nome_peca)}</td><td>${escapeHTML(part.categoria)}</td><td>${currencyBRL.format(part.custo_unitario)}</td><td>${integerBR.format(part.estoque_atual)}</td><td class="text-end text-nowrap"><button class="btn btn-sm btn-outline-primary me-1" data-edit-part="${escapeHTML(part.sku)}" title="Editar peça"><i class="bi bi-pencil" aria-hidden="true"></i><span class="visually-hidden">Editar</span></button><button class="btn btn-sm btn-outline-danger" data-delete-part="${escapeHTML(part.sku)}" title="Excluir peça"><i class="bi bi-trash" aria-hidden="true"></i><span class="visually-hidden">Excluir</span></button></td></tr>`,
        )
        .join("")
    : '<tr><td colspan="6" class="empty-state py-4 text-center">Nenhuma peça cadastrada.</td></tr>';
}

function saleNetValue(sale) {
  return sale.quantidade * sale.preco_unitario * (1 - sale.desconto / 100);
}

function renderSales() {
  elements.salesCount.textContent = `${integerBR.format(state.sales.length)} registros`;
  elements.salesTable.innerHTML = state.sales.length
    ? state.sales
        .map(
          (sale) =>
            `<tr><td class="sku">${escapeHTML(sale.id_venda)}</td><td>${escapeHTML(sale.data_venda)}</td><td>${escapeHTML(sale.loja)}</td><td>${escapeHTML(sale.sku)}</td><td>${integerBR.format(sale.quantidade)}</td><td>${currencyBRL.format(saleNetValue(sale))}</td><td><span class="badge ${sale.status === "CONCLUIDA" ? "text-bg-success" : "text-bg-secondary"}">${escapeHTML(sale.status)}</span></td><td class="text-end text-nowrap"><button class="btn btn-sm btn-outline-primary me-1" data-edit-sale="${escapeHTML(sale.id_venda)}" title="Editar venda"><i class="bi bi-pencil" aria-hidden="true"></i><span class="visually-hidden">Editar</span></button><button class="btn btn-sm btn-outline-danger" data-cancel-sale="${escapeHTML(sale.id_venda)}" title="Cancelar venda"><i class="bi bi-x-circle" aria-hidden="true"></i><span class="visually-hidden">Cancelar</span></button></td></tr>`,
        )
        .join("")
    : '<tr><td colspan="8" class="empty-state py-4 text-center">Nenhuma venda registrada.</td></tr>';
}

function populateFilters() {
  const stores = [...new Set(state.sales.map((sale) => sale.loja))].sort();
  const categories = [
    ...new Set(state.parts.map((part) => part.categoria)),
  ].sort();
  elements.filterStore.innerHTML =
    '<option value="">Todas as lojas</option>' +
    stores
      .map(
        (store) =>
          `<option value="${escapeHTML(store)}">${escapeHTML(store)}</option>`,
      )
      .join("");
  elements.filterCategory.innerHTML =
    '<option value="">Todas as categorias</option>' +
    categories
      .map(
        (category) =>
          `<option value="${escapeHTML(category)}">${escapeHTML(category)}</option>`,
      )
      .join("");
}

function renderInsights() {
  const partBySku = new Map(state.parts.map((part) => [part.sku, part]));
  const start = elements.filterStart.value;
  const end = elements.filterEnd.value;
  const store = elements.filterStore.value;
  const category = elements.filterCategory.value;
  const filteredSales = state.sales.filter((sale) => {
    const part = partBySku.get(sale.sku);
    return (
      sale.status === "CONCLUIDA" &&
      (!start || sale.data_venda >= start) &&
      (!end || sale.data_venda <= end) &&
      (!store || sale.loja === store) &&
      (!category || part?.categoria === category)
    );
  });
  const revenue = filteredSales.reduce(
    (total, sale) => total + saleNetValue(sale),
    0,
  );
  const cost = filteredSales.reduce(
    (total, sale) =>
      total + sale.quantidade * (partBySku.get(sale.sku)?.custo_unitario || 0),
    0,
  );
  const grouped = {};
  filteredSales.forEach((sale) => {
    const name = partBySku.get(sale.sku)?.categoria || "DESCONHECIDA";
    grouped[name] ||= { revenue: 0, cost: 0 };
    grouped[name].revenue += saleNetValue(sale);
    grouped[name].cost +=
      sale.quantidade * (partBySku.get(sale.sku)?.custo_unitario || 0);
  });
  elements.insightsSummary.innerHTML = `<div class="col-12 col-md-4"><div class="insight-stat"><span>Faturamento filtrado</span><strong>${currencyBRL.format(revenue)}</strong></div></div><div class="col-12 col-md-4"><div class="insight-stat"><span>Margem estimada</span><strong>${currencyBRL.format(revenue - cost)}</strong></div></div><div class="col-12 col-md-4"><div class="insight-stat"><span>Vendas concluídas</span><strong>${integerBR.format(filteredSales.length)}</strong></div></div>`;
  const rows = Object.entries(grouped).sort(
    ([, first], [, second]) => second.revenue - first.revenue,
  );
  elements.marginContent.innerHTML = rows.length
    ? `<table class="table table-hover mb-0"><caption class="visually-hidden">Margem estimada por categoria</caption><thead><tr><th>Categoria</th><th>Faturamento</th><th>Custo</th><th>Margem estimada</th></tr></thead><tbody>${rows.map(([name, values]) => `<tr><td class="fw-semibold">${escapeHTML(name)}</td><td>${currencyBRL.format(values.revenue)}</td><td>${currencyBRL.format(values.cost)}</td><td class="text-success fw-bold">${currencyBRL.format(values.revenue - values.cost)}</td></tr>`).join("")}</tbody></table>`
    : '<p class="empty-state mb-0">Nenhuma venda concluída corresponde aos filtros.</p>';
}

function resetPartForm() {
  state.editingPartSku = null;
  elements.partForm.reset();
  elements.partFormTitle.textContent = "Adicionar peça";
  document.getElementById("part-sku").disabled = false;
}
function startPartEdit(sku) {
  const part = state.parts.find((item) => item.sku === sku);
  if (!part) return;
  state.editingPartSku = sku;
  elements.partFormTitle.textContent = `Editar peça ${sku}`;
  document.getElementById("part-sku").value = part.sku;
  document.getElementById("part-sku").disabled = true;
  document.getElementById("part-name").value = part.nome_peca;
  document.getElementById("part-category").value = part.categoria;
  document.getElementById("part-cost").value = part.custo_unitario;
  document.getElementById("part-supplier").value = part.fornecedor;
  document.getElementById("part-stock").value = part.estoque_atual;
  document.getElementById("parts-view").scrollIntoView({ behavior: "smooth" });
}
function startSaleEdit(id) {
  const sale = state.sales.find((item) => item.id_venda === id);
  if (!sale) return;
  state.editingSaleId = id;
  elements.saleEditor.classList.remove("d-none");
  document.getElementById("sale-editor-id").textContent = id;
  document.getElementById("sale-date").value = sale.data_venda;
  document.getElementById("sale-store").value = sale.loja;
  document.getElementById("sale-client").value = sale.cliente;
  document.getElementById("sale-sku").value = sale.sku;
  document.getElementById("sale-quantity").value = sale.quantidade;
  document.getElementById("sale-price").value = sale.preco_unitario;
  document.getElementById("sale-discount").value = sale.desconto;
  document.getElementById("sale-status").value = sale.status;
  document.getElementById("sale-seller").value = sale.vendedor;
  elements.saleEditor.scrollIntoView({ behavior: "smooth" });
}

async function loadData() {
  setLoading(true);
  elements.error.classList.add("d-none");
  elements.status.textContent = "Consultando os dados mais recentes...";
  try {
    const [revenue, categories, inventory, parts, sales] = await Promise.all([
      requestJSON("/dashboard/faturamento-total"),
      requestJSON("/dashboard/faturamento-por-categoria"),
      requestJSON("/dashboard/estoque-parado"),
      requestJSON("/pecas/"),
      requestJSON("/vendas/"),
    ]);
    state.parts = parts;
    state.sales = sales;
    renderDashboard(revenue, categories, inventory);
    renderParts();
    renderSales();
    populateFilters();
    renderInsights();
    elements.status.textContent = "Dados carregados com sucesso.";
  } catch (error) {
    console.error("Falha ao carregar dados:", error);
    elements.error.textContent = `Não foi possível carregar os dados. ${error.message}`;
    elements.error.classList.remove("d-none");
    elements.status.textContent = "A atualização não foi concluída.";
  } finally {
    setLoading(false);
  }
}

async function savePart(event) {
  event.preventDefault();
  const sku = document.getElementById("part-sku").value.trim().toUpperCase();
  const payload = {
    sku,
    nome_peca: document.getElementById("part-name").value.trim().toUpperCase(),
    categoria: document
      .getElementById("part-category")
      .value.trim()
      .toUpperCase(),
    custo_unitario: Number(document.getElementById("part-cost").value),
    fornecedor: document
      .getElementById("part-supplier")
      .value.trim()
      .toUpperCase(),
    estoque_atual: Number(document.getElementById("part-stock").value),
  };
  try {
    await requestJSON(
      state.editingPartSku
        ? `/pecas/${encodeURIComponent(state.editingPartSku)}`
        : "/pecas/",
      {
        method: state.editingPartSku ? "PUT" : "POST",
        body: JSON.stringify(payload),
      },
    );
    resetPartForm();
    await loadData();
  } catch (error) {
    showActionError(error);
  }
}
async function deletePart(sku) {
  if (!window.confirm(`Excluir a peça ${sku}?`)) return;
  try {
    await requestJSON(`/pecas/${encodeURIComponent(sku)}`, {
      method: "DELETE",
    });
    await loadData();
  } catch (error) {
    showActionError(error);
  }
}
async function saveSale(event) {
  event.preventDefault();
  if (!state.editingSaleId) return;
  const payload = {
    id_venda: state.editingSaleId,
    data_venda: document.getElementById("sale-date").value,
    loja: document.getElementById("sale-store").value.trim().toUpperCase(),
    cliente: document.getElementById("sale-client").value.trim().toUpperCase(),
    sku: document.getElementById("sale-sku").value.trim().toUpperCase(),
    quantidade: Number(document.getElementById("sale-quantity").value),
    preco_unitario: Number(document.getElementById("sale-price").value),
    desconto: Number(document.getElementById("sale-discount").value),
    status: document.getElementById("sale-status").value,
    vendedor: document.getElementById("sale-seller").value.trim().toUpperCase(),
  };
  try {
    await requestJSON(`/vendas/${encodeURIComponent(state.editingSaleId)}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
    cancelSaleEdit();
    await loadData();
  } catch (error) {
    showActionError(error);
  }
}
async function cancelSale(id) {
  if (!window.confirm(`Cancelar a venda ${id}?`)) return;
  try {
    await requestJSON(`/vendas/${encodeURIComponent(id)}`, {
      method: "DELETE",
    });
    await loadData();
  } catch (error) {
    showActionError(error);
  }
}
function cancelSaleEdit() {
  state.editingSaleId = null;
  elements.saleEditor.classList.add("d-none");
  elements.saleForm.reset();
}
function showActionError(error) {
  elements.error.textContent = `Não foi possível concluir a operação. ${error.message}`;
  elements.error.classList.remove("d-none");
}

document.querySelectorAll(".workspace-tab").forEach((tab) =>
  tab.addEventListener("click", () => {
    document
      .querySelectorAll(".workspace-tab")
      .forEach((item) => item.classList.toggle("active", item === tab));
    document
      .querySelectorAll(".app-view")
      .forEach((view) =>
        view.classList.toggle("d-none", view.id !== tab.dataset.view),
      );
    document
      .getElementById("insights-panel")
      .classList.toggle("d-none", tab.dataset.view !== "dashboard-view");
  }),
);
document
  .getElementById("insights-filters")
  .addEventListener("submit", (event) => {
    event.preventDefault();
    renderInsights();
  });
document.getElementById("clear-filters").addEventListener("click", () => {
  document.getElementById("insights-filters").reset();
  renderInsights();
});
document.getElementById("new-part").addEventListener("click", resetPartForm);
document.getElementById("cancel-part").addEventListener("click", resetPartForm);
elements.partForm.addEventListener("submit", savePart);
elements.saleForm.addEventListener("submit", saveSale);
document
  .getElementById("cancel-sale")
  .addEventListener("click", cancelSaleEdit);
elements.partsTable.addEventListener("click", (event) => {
  const edit = event.target.closest("[data-edit-part]");
  const remove = event.target.closest("[data-delete-part]");
  if (edit) startPartEdit(edit.dataset.editPart);
  if (remove) deletePart(remove.dataset.deletePart);
});
elements.salesTable.addEventListener("click", (event) => {
  const edit = event.target.closest("[data-edit-sale]");
  const cancel = event.target.closest("[data-cancel-sale]");
  if (edit) startSaleEdit(edit.dataset.editSale);
  if (cancel) cancelSale(cancel.dataset.cancelSale);
});
elements.refresh.addEventListener("click", loadData);
loadData();
