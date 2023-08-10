
def parse_qq_launcher(launcher: str) -> tuple[str, int]:
    lspt = launcher.split('_')
    return lspt[0], int(lspt[1])
