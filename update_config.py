import os
import yaml

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Get current working directory
    config['project_root_dir'] = os.getcwd()

    with open('config.yaml', 'w') as f:
        yaml.dump(config, f)
