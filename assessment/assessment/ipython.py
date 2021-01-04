def load_ipython_extension():
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    try:
        import os, sys
        sys.path.insert(0, '~/assessment')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assessment.settings")
        import django
        django.setup()
    except ImportError:
        pass

if __name__ == "__main__":
    load_ipython_extension()