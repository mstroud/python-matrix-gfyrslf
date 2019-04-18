gfyrslf
=====================
A simple, extensible Python 3 [Matrix](https://matrix.org) bot.

Requires the [matrix-python-sdk](https://github.com/matrix-org/matrix-python-sdk) matrix-client module.

Setup
----------
    % python setupy.py install
    % cp config.yml.dist config.yml
    (edit config.yml to suit your application...)
    
Usage
-----------

    from gifyrslf import GfyrslfBot 
    
    # Create an instance of GfyrslfBot
    gbot = GfyrslfBot(cfg='config.yml')

    # Start polling for room events
    gbot.run()

    