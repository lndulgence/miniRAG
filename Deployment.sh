# A microk8s cluster with an enabled image registry is required to run this script!!!
cd model && bash makeservicesh.sh && cd ..
cd RagAPI && bash makeservicesh.sh && cd ..
cd mainAPI && bash makeservicesh.sh && cd ..