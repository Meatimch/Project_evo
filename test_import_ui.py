import traceback, sys
try:
    m = __import__('ui.main_window', fromlist=['*'])
    print('Imported OK, has MainWindow =', hasattr(m, 'MainWindow'))
except Exception:
    traceback.print_exc()
    sys.exit(1)
