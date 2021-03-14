function deleteNote(id) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ cv_id: id }),
  }).then((_res) => {
    window.location.href = "/matching";
  });
}
