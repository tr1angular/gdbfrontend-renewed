document.addEventListener('DOMContentLoaded', function() {
  const editor = document.getElementById('codeEditor');
  const consoleInput = document.getElementById('consoleInput');
  const consoleOutput = document.getElementById('consoleOutput');
  const fileInput = document.getElementById('fileUpload');
  const gdbRun = document.getElementById('gdbRun');

  // breakpoints setter
  editor.addEventListener('click', function(event) {
    const codeLine = event.target.closest('.code-line');
    if (codeLine) {
      codeLine.classList.toggle('breakpoint');
    }
  });

  // gdb console handler
  gdbRun.addEventListener('click', function() {
    const command = consoleInput.textContent;
    console.log(command);
    $.ajax({
      type: 'POST',
      url: '/execute_command',
      data: { command: command, filename: fileInput.files[0] },
      success: function(response) {
        console.log(response);

        const payloads = response
        .filter(function (obj) {
            return obj.hasOwnProperty('payload') && typeof obj.payload === 'string';
        })
        .map(function (obj) {
            return obj.payload;
        });

        payloads.forEach(function(value) {
            if (!isNaN(value.charAt(0))) {
                $('.code-line').removeClass('breakpoint');
                const lineNumber = parseInt(value.charAt(0)) + 1;
                const codeLine = document.querySelector(`[data-line-number="${lineNumber}"]`);

                if (codeLine) {
                    codeLine.classList.add('breakpoint');
                }
            }
        });

        consoleOutput.innerHTML = payloads.join('<br>');
      },
      error: function(error) {
        console.log('Error:', error);
      }
    });
  });

  // File uploading handler
  fileInput.addEventListener('change', function() {
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
        editor.textContent = result;
    })
    .catch(error => console.error('Error:', error));
  });
});
