
form = document.getElementById("updatePropertyForm");
function updatePropertyForm(id, name, address) {
  fetch("/update_property/" + id, {
    method: "PATCH",
    body: JSON.stringify({
      name,
      address,
    }),
  }).then((response) => response.json());
  window.location.reload();
}

form.addEventListener("submit", (e) => {
   alert('hey updating..')
  e.preventDefault();
  alert('hey updating..')
  const name = document.getElementById("name").value;
  const address = document.getElementById("address").value;
  const id = document.getElementById("id").value;
  updatePropertyForm(id, name, address);
});