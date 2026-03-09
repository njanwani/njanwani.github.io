function toggleblock(id) {
  var block = document.getElementById(id);
  if (block === null) return;
  
  if (block.style.display === 'none' || block.style.display === '') {
    block.style.display = 'block';
  } else {
    block.style.display = 'none';
  }
}
