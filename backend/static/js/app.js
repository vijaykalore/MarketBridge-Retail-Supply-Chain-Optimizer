async function fetchProducts(){
  const r = await fetch('/api/products');
  return await r.json();
}

async function fetchInventory(){
  const r = await fetch('/api/inventory');
  return await r.json();
}

export async function initUI(){
  const prodSel = document.getElementById('product-select');
  const prodList = await fetchProducts();
  prodSel.innerHTML = '';
  prodList.forEach(p=>{ const o = document.createElement('option'); o.value=p.id; o.textContent=p.name; prodSel.appendChild(o); })
  await renderInventory();
}

export async function renderInventory(){
  const items = await fetchInventory();
  const tbody = document.querySelector('#inventory-table tbody'); tbody.innerHTML = '';
  if(!items.length){ tbody.innerHTML = '<tr><td colspan="6" class="small">No inventory records</td></tr>'; return }
  for(const i of items){
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${i.id}</td>
      <td>${i.product_id}</td>
      <td>${i.location_id}</td>
      <td>${i.quantity}</td>
      <td>${i.last_updated}</td>
      <td class="row-actions"><button data-pid="${i.product_id}" class="predict">Predict</button></td>`;
    tbody.appendChild(tr);
  }
}

export function showToast(msg){
  const t = document.createElement('div'); t.className='toast'; t.textContent=msg; document.body.appendChild(t);
  setTimeout(()=>t.remove(),3000);
}

document.addEventListener('submit', async e=>{
  if(e.target.id==='product-form'){
    e.preventDefault(); const body=Object.fromEntries(new FormData(e.target).entries());
    const r = await fetch('/api/product',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
    const j = await r.json(); if(r.status==201) showToast('Created product '+j.name); await initUI();
  }
  if(e.target.id==='inventory-form'){
    e.preventDefault(); const body=Object.fromEntries(new FormData(e.target).entries()); body.quantity = Number(body.quantity);
    const r = await fetch('/api/inventory',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
    const j = await r.json(); if(r.status==201) showToast('Added inventory id '+j.id); await renderInventory();
  }
});

document.addEventListener('click', async e=>{
  if(e.target.matches('.predict')){
    const pid = e.target.dataset.pid; const r = await fetch('/api/predict/'+pid); const j = await r.json();
    showToast(`Product ${pid}: recommend ${j.recommended_restock}`);
  }
  if(e.target.id==='refresh') await renderInventory();
  if(e.target.id==='export-csv'){
    const items = await fetchInventory(); if(!items.length) return showToast('No data');
    const csv = [Object.keys(items[0]).join(',')].concat(items.map(i=>Object.values(i).join(','))).join('\n');
    const blob = new Blob([csv],{type:'text/csv'}); const url = URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='inventory.csv'; document.body.appendChild(a); a.click(); a.remove();
  }
});

window.addEventListener('load', ()=>initUI());
