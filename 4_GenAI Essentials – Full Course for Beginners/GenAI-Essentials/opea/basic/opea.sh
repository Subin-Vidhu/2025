# Install Docker
git clone https://github.com/opea-project/GenAIExamples.git
cd GenAIExamples/ChatQnA/docker_compose
chmod +x ./install_docker.sh
./install_docker.sh
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Set Envs
export HUGGINGFACEHUB_API_TOKEN="SET_KEY"
export host_ip=$(hostname -I | awk '{print $1}')
export no_proxy="localhost"
cd intel/cpu/xeon

# Use llama model instead of neural chat
sed -i 's/Intel/meta-llama/g' ./set_env.sh
sed -i 's/neural-chat-7b-v3-3/Llama-3.2-1B-Instruct/g' ./set_env.sh
chmod +x ./set_env.sh
source ./set_env.sh

# Start Docker
docker compose -f compose.yaml up -d