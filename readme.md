# Distributed Image Processing App

The Distributed Image Processing App is a cloud-based application designed to efficiently process and manage large volumes of image data. It leverages various   AWS services, including S3 for storage, RabbitMQ for message queueing, and Python for backend processing. The user interface is built using React and Flask, providing a simple uploading interface for users to submit images for processing.


## User guide:
End users need no configurations. just visit the site and start using it.

## Project Structure

- `.env.example`: Example environment configuration file.
- `components/`: Source code directory containing the main application scripts and configuration files.
- `config/`:contain the main application  configuration files.



## Usage


### Environment Configuration

1. Create a `.env` file in the directories of both the master and executor components.
2. Copy the content of `.env.example` into your `.env` file.
3. Modify the `.env` file to fit your specific configuration (e.g., paths, credentials, etc.).

### Systemd Services Configuration

1. There are three types of configuration scripts for different machine roles:
   - `worker-node-config.sh`: Configuration for worker machines.
   - `server-node-config.sh`: Configuration for server machines.
   - `broker-node-config.sh`: Configuration for broker machines.
1. Adjust the execution paths in each script to match your deployment.
2. Run the respective script on each machine to set up the systemd service:

    ```bash
    sudo ./daemonize_worker.sh
    sudo ./daemonize_server.sh
    ```

## Configuration Files

- **Worker Configuration File:** Located in `config/worker-node-config.sh`. Contains specific settings for worker nodes.
- **Server Configuration File:** Located in `config/server-node-config.sh`. Contains specific settings for server nodes.
- **Broker Configuration File:** Located in `config/broker-node-config.sh`. Contains specific settings for broker nodes.

## Automatic Service Management

The project includes systemd service configurations to ensure that the application runs automatically on boot and restarts on failure.

1. **Worker Service:**
   - Configured via `configure_worker.sh`.
   - Service description: `docker-worker-compose`.

2. **Server Service:**
   - Configured via `configure_server.sh`.
   - Service description: `docker-compose`.

3. **Broker Service:**
   - Configured via `broker-node-config`.

To enable and start the services manually:

```bash
sudo systemctl enable docker-worker-compose
sudo systemctl start docker-worker-compose

sudo systemctl enable docker-compose
sudo systemctl start docker-compose

```
## Demos:

- [A request journey](https://youtu.be/t7klgqfw-MM?si=7a5XFA_2CrL7Fy3P)
- [Advanced processing (MPI in action)](https://youtu.be/9XxUw2MiONM?si=-3uBCy83-uo0O7l2) 
- [Configuration](https://youtu.be/jvSPu5B_ogk?si=V5A7EH9-ez6D2_9r)
