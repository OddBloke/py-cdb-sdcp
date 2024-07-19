# py-cbd-sdcp

This repo contains a nascent Python client for the recently open source'd [SDCP
3.0](https://github.com/cbd-tech/SDCP-Smart-Device-Control-Protocol-V3.0.0/blob/main/SDCP%28Smart%20Device%20Control%20Protocol%29_V3.0.0_EN.md)
3D printer control protocol for printers using CBD firmware (e.g. the Elegoo
Mars 5 Ultra).

It is not intended for any sort of real usage, but I wanted to make my
investigatory work available for anyone else who's interested.

## Observed Issues

* I have seen enabling the camera via the API and then connecting to the RTSP
  server multiple times cause the printer's web interface and on-screen UI to
  hang
