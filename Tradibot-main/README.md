# Tradibot

Un motor de trading algorítmico de alta frecuencia construido en Python. Diseñado para detectar explosiones de *momentum* en el mercado de valores en tiempo real y ejecutar operaciones automatizadas utilizando la API de Alpaca.

##  Arquitectura del Sistema

El bot está diseñado con una arquitectura modular que separa la lógica de detección de la ejecución de órdenes:

**Motor de Momentum (`momentum_motor.py`):** Utiliza WebSockets (`asyncio`) para consumir el flujo de datos IEX en tiempo real. Implementa una cola de doble extremo (`collections.deque`) como memoria temporal y eficiente para analizar la aceleración del precio y saltos de volumen.
**Ejecutor Táctico (`ejecutor.py`):** Maneja la comunicación REST con el broker. Al recibir la señal del motor, ensambla y dispara una *Bracket Order* (Orden de Compra + Take Profit + Stop Loss) en un solo paquete de red para asegurar la gestión de riesgo al milisegundo.

##  OpSec y Seguridad

Las credenciales de la API están estrictamente aisladas del código fuente. Se utiliza `python-dotenv` para inyectar las llaves públicas y privadas directamente en la memoria del entorno virtual al momento de ejecución, previniendo filtraciones en el repositorio.

##  Instalación y Despliegue

**1. Clonar el repositorio:**
```
git clone [https://github.com/ReyMD9/Tradibot.git](https://github.com/ReyMD9/Tradibot.git)
cd Tradibot
```
2. Levantar el entorno virtual aislado:
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias operativas:
```
pip install alpaca-trade-api python-dotenv requests
```

5. Configurar la bóveda de credenciales:
Crea un archivo llamado .env en la raíz del proyecto y añade tus llaves de Alpaca (Paper Trading)
```

ALPACA_API_KEY=tu_llave_publica_aqui
ALPACA_SECRET_KEY=tu_llave_privada_aqui
```
**Uso**

Para iniciar el patrullaje del mercado en tiempo real, ejecuta el motor principal. El bot se conectará al stream de datos y quedará a la espera de anomalías matemáticas para disparar:
```
python3 momentum_motor.py
```
**Disclaimer: Este código tiene fines estrictamente educativos y de investigación tecnológica. Las estrategias algorítmicas conllevan un alto riesgo. Utilizar únicamente en entornos de simulación (Paper Trading)**
