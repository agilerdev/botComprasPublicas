const fs = require('fs');
const cron = require('node-cron');
const express = require('express');


function script() {
  const bot = require('./bot.js');
  const { spawn } = require('child_process');
  const childPython = spawn('python3', ['script.py']);
  console.log('Ejecutando script');
  childPython.stdout.on('data', async (data) => {
    console.log(`stdout: ${data}`);
    if (data == 1) {
      let rawdata = fs.readFileSync('./datos.json');
      console.log(rawdata);

      let datos = JSON.parse(rawdata);


      console.log(datos);
      for (let i = 0; i < datos.length; i++) {
        let mensaje = "Nueva contratación!" + "\n" + datos[i].texto + "\n" + datos[i].link;
        await bot.enviar(mensaje);
      }
    }
    console.log('se ejecuto el script')
    return;
  });
  console.log('se termino');
  return;
}



cron.schedule('*/30 * * * *', () => {
  script();
});

const app = express();

app.listen(3939, null, () => {
  script();
});