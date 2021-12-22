import typer
from ancs4linux.common.dbus import EventLoop, SystemBus
from ancs4linux.observer.server import ObserverServer
from ancs4linux.observer.mobile_scanner import MobileScanner


def main(
    observer_dbus: str = typer.Option("ancs4linux.Observer", help="Service path")
) -> None:
    loop = EventLoop()

    server = ObserverServer()
    scanner = MobileScanner(server)
    server.register()
    SystemBus().register_service(observer_dbus)

    print("Observing devices")
    scanner.start_observing()
    loop.run()


def cli() -> None:
    typer.run(main)