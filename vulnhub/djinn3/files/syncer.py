from configuration import *
from connectors.ftpconn import *
from connectors.sshconn import *
from connectors.utils import *

def main():
    """Main function
    Cron job is going to make my work easy peasy
    """
    configPath = ConfigReader.set_config_path()
    config = ConfigReader.read_config(configPath)
    connections = checker(config)
    if 'FTP' in connections:
        ftpcon(config['FTP'])
    else:
        if 'SSH' in connections:
            sshcon(config['SSH'])
        else:
            if 'URL' in connections:
                sync(config['URL'], config['Output'])


if __name__ == '__main__':
    main()
