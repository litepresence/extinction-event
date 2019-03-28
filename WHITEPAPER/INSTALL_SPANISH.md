INSTALACIÓN
=======================
**EXTINCTION EVENT - CEX MUST DIE**

NOTA: este conjunto de herramientas se encuentra actualmente en estado alfa, aún en desarrollo; ¡pronto habrá más juguetes nuevos!

**(BTS) litepresence1**

**Herramientas de trading BitShares DEX**

La traducciónd del nombre significa "Evento de Extinción Masiva" y  nació de la idea de que combinación de la tecnología DEX con la disposición del usuario común de tecnología de trading controlada por inteligencia artificial, supondrá un evento de nivel de extinción masiva tanto para las mercados centralizados (CEX) basados en la web como para los servicios de trading algorítmicos de "cuota mensual".


**REÚNE EL HARDWARE**

Este desarrollo es intensivo en lectura/escritura de datos, se hace necesario un disco SSD, al menos de 4 gigabytes de RAM y una cpu rápida para conseguir una adecuada velocidad en los backtest.

Recomendaciones:

- SSD (SOLID STATE DRIVE) de cualquier tamaño; una unidad de 120 GB que cuesta poco mas de 20 euros es suficiente.
- NO instales exinction-event en un disco duro convencional.
- Mínimo 4 GB RAM para un desempeño adecuado, preferiblemente 8 GB.
- Una CPU de escritorio de nivel medio a alto, yo utilizo un AMD 7950.
- Fuente de alimentación con certificación 80PLUS Platino u Oro, ya que el bot estará corriendo las 24 horas.


**INSTALA LINUX**

Cualquier debian/ubuntu podría servir.  
NO es compatible con Mac o Windows
Yo uso Cinnamon Mint 19.04, para más información visita:

    https://linuxmint.com/

extinction-event debería ser compatible con otras distribuciones de linux, pero cada instalación puede variar. 

**ACTUALIZA APT-GET**

    sudo apt-get update

**INSTALA PYTHON 3.6 O SUPERIOR**

Por ejemplo ejecutando este comando:

    https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/

**INSTALA LAS APLICACIONES NECESARIAS**

    sudo apt-get install - python3-pip
    sudo apt-get install python3-tk
    sudo apt-get install python3-dev
    sudo apt-get install libsecp256k1-dev
    sudo apt-get install git
    sudo pip3 install virtualenv

**ClONA EL REPOSITORIO GIT DE EXTINCTION EVENT**

Navegamos hasta la carpeta desde la que desea ejecutar:

    $ cd <nombre de la carpeta>
    $ git clone https://github.com/litepresence/extinction-event.git

**CREAR UN ENTORNO VIRTUAL**

Abrimos la carpeta de eventos de extinción y lo ejecutamos desde allí:

    $ .../extinction-event
    $ virtualenv -p python3 env 

**ACTIVAR EL ENTORNO VIRTUAL**

    $ source env/bin/activate

**INSTALAMOS LOS MODULOS DEL ARCHIVO DE REQUERIMIENTOS**

    pip install -r requirements.txt
    
*NOTAS:* El entorno virtual y setup.py están en la carpeta `extinction-event`.
Los scripts están todos en `extinction-event/EV`.
Necesitarás activar el entorno virtual desde la carpeta de `extinction-event` CADA VEZ que inicies una nueva terminal para ejecutar estos scripts.

**TEST DE LATENCIA**

Abre una nueva ventana de la terminal. Ejecuta el script del test de latencia, tardará unos minutos. Generará el archivo nodes.txt que será usado por metaNODE.py.  Navegar a la carpeta y ejecutalo.

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 latencyTEST.py

Cuando ejecutes a tiempo completo el bot de modo mas serio, puedes cambiar `USER CONTROLS` dentro de latencyTEST.py para un bucle recurrente, crear listas de permisos personalizadas, o para escanear github en busca de nodos recién publicados. Incluso puede hacer graficas las ubicaciones de los nodos y subir los resultados a internet.  Después de que la prueba de latencia haya generado node.txt, abre el archivo node.txt en un editor de texto para confirmar que contiene una lista de nodos ordenados por latencia para tu región.

**METÁ NODO**

A continuación, comenzará tu primera sesión de metaNODE.  Abre una terminal, usa 'cd' para  navegar hasta la carpeta y ejecutalo.

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 metaNODE.py
	
Ingresa tu cuenta y el mercado DEX de tu elección, o puedes presionar enter para omitir este paso y se elegirá una cuenta y un mercado predeterminados:

```
account: abc123
currency: open.btc
assest: bts
```

La capitalización no importa para el activo y la moneda. metaNODE NO PUEDE acceder a sus fondos.


**MICRO DEX**

Te permite asegurarte de que tienes todas las dependencias para firmar las transacciones instaladas.  En una nueva ventana de terminal, con metaNODE todavía ejecutándose en la primera terminal, navega la carpeta y ejecutalo.

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 microDEX.py

Te dará la OPCIÓN de ingresar tu WIF. Puedes pulsar ENTER para omitirlo.  NO necesitas dar tu WIF en este momento para asegurar una configuración completa. 

*microDEX TIENE ACCESO COMPLETO A TUS FONDOS SI FACILITAS TU WIF*

DEBES familiarizarte y familiarizar a sus amigos con el código fuente antes de ingresar tu WIF.  Tu WIF es lo que firma transacciones de cualquier tipo.  NO DEBES autentificar a menos que entiendas y confíes plenamente en los scripts que te he dado.

La mejor manera de obtener tu WIF es abriendo la referencia Bitshares UI:

ajustes >> cuentas >> mostrar claves
clic en el icono "CLAVE
clic en "mostrar clave privada en formato WIF".

para obtener una copia de la interfaz de referencia, visita:

http://bitshares.org/download/

**APIKEYS**

La última versión permite hacer backtests con datos del DEX de bitshares así como usar otras varias fuentes.  Cada una de estas fuentes fue elegida por la gran cantidad de datos disponibles y facilitar claves para sus API de forma GRATUITA. 

Puedes conseguir claves para las API de: 

www.cryptocompare.com

www.alphavantage.com

www.nomics.com

Edita apiKEYS.py e completa el diccionario con las claves, guarda el archivo y cierralo.

*NOTA: Este archivo py debe estar en formato json*
- Usa dobles comillas y una coma después de cada entrada, excepto la última, esa va sin coma.
- NO incluyas ningún comentario u otro texto en este documento.

Estas claves son de api públicas y NO PUEDEN afectar tus fondos si son robadas. Sin embargo cada clave tiene limites de llamadas diarias a la api, conservalas a salvo para prevenir ataques de denegación de acceso.  Necesitan ser mantenidas en privado; pero no pueden poner en peligro los fondos de capital, como si ocurre con el WIF.  Consulta cada sitio web para obtener más detalles.

Si omites este paso, sólo podrás realizar backtests con `CANDLE_SOURCE = 'DEX'` en `tune_install()`, ya que los nodos llamada de procedimiento remoto públicos de BitShares no requieren claves de API. 

**PROXY TEST***

proxyTEST.py se asegurará de que has instalado correctamente tus claves api para backtest.

Abre proxyTEST, encontrarás una entrada `API` cerca de la parte superior del script.  Haga una prueba con los números del 1 al 6 de `API`. 

**EXTINCTION EVENT**

En una nueva terminal, con metaNODE todavía ejecutándose en la primera terminal, navega hasta la carpeta y ejetula el script.

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 extinctionEVENT.py

Se te ofrecerán algunas opciones:

**BACKTEST** 

permite probar y ajustar estrategias usando la definición `tune_install()` dentro de extictionEVENT.py

**PAPER** 

permite ejecutar una sesión en tiempo real sin darle al bot sus claves, no se realizarán operaciones reales.

**LIVE** 

es el comercio en vivo con fondos según su configuración de `control_panel()` y `tune_install()`.

**SALES** 

permite vender ajuestes de estrategias de extinctionEVENT, publicando imágenes de los puntos operados, pero sin mostrar tus umbrales para la media móvil.

**ORDER_TEST** 

sesión de operaciones en vivo con dinero real.  Sin embargo, coloca las ordenes lejos de los márgenes,  para probar sólo la autenticación.

**OPTIMIZER** 

ajuste automático para los parametros del backtest. Actualmente NO es  código abierto; de hecho estoy considerando un trabajador para esto y algo más.

**HISTORIAL DE LA CUENTA**

Cada vez que tu metaNODO se está ejecutando, el historial de tu cuenta se registra en un archivo. accountHISTORY.py puede leer este archivo y graficar la evolución de los saldos de la cuenta. 

**BREVE DESCRIPCIÓN DE LAS HERRAMIENTAS**

**extinciónEVENT.py**

Framework para el bot de trading algoritmico basado en el cruce de medias para operar en el DEX de Bitshares.  Permite realizar tanto backtest como trading real.

**microDEX.py**

Interfaz de usuario ligera para realizar operaciones manuales de compra/venta/cancelación en el DEX de Bitshares

**metaNODE.py**

Conservación estadística de datos de mercado de múltiples nodos DEX públicos en un archivo de texto en streaming

**latencyTEST.py**

Busca nodos Bitshares de baja latencia en tu zona

**proxyDEX.py**

Velas en formato HLOCV del DEX de Bitshares, correctamente interpoladas para backtest y trading real

**proxyCEX.py**

Velas diarias altcoin de cryptocompare.com en formato HLOCV para backtest

**proxyMIX.py**

Velas diarias de crypto exchanges de nomics.com en formato HLOCV para backtest

**proxyALPHA.py**

Velas diarias de acciones, forex y crypto:forex de alphavantage.com en formato HLOCV para backtest

**apiKEYS.py**

Diccionario para almacenar sus claves API de cryptocompare, alphavantage y nomics

**proxyTEST.py**

Utilidad para recopilar y graficar datos de proxyDEX.py, proxyCEX.py, proxyMIX.py y proxyALPHA.py

**accountHISTORY.py**

metaNODE.py registra los balances cada hora mientras se está ejecutando, utiliza accountHISTORY para visualizarlas.

**Visite www.litepresence.com para obtener algoritmos optimizados para máquinas**

Ejecuto cientos de miles de pruebas usando enjambres de partículas cuánticas cultivadas elitistamente,  para optimizar los algoritmos.
Tu mismo puedes optimizar los algoritmos por ensayo y error, pero ¿por qué no dejar que mi IA se encargue de ello?

**www.litepresence.com**


*Traducción versión 0.1,  por Paduel.*


