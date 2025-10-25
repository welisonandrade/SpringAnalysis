# Este é o seu locustfile.py 
import random
from locust import HttpUser, task, between

class PetClinicUser(HttpUser):
    # Usuários vão esperar entre 1 e 3 segundos entre as tarefas
    wait_time = between(1, 3) 
    
    # Lista de IDs de donos para usar no teste GET /owners/{id}
    owner_ids = []

    def on_start(self):
        """
        Isso é executado quando um usuário virtual inicia.
        Vamos usá-lo para buscar IDs válidos.
        """
        try:
            # Busca a lista de donos 
            response = self.client.get("/api/customer/owners")
            response.raise_for_status() # Garante que a requisição foi um sucesso
            
            owners = response.json()
            if owners:
                # Extrai os IDs da resposta
                self.owner_ids = [owner['id'] for owner in owners]
            
            if not self.owner_ids:
                print("Aviso: Não foi possível buscar IDs de donos. O teste GET /owners/{id} pode falhar.")
                # Se falhar, usamos uma lista padrão (ex: os IDs que você anotou na Fase 2)
                self.owner_ids = [1, 2, 3, 4, 5] 

        except Exception as e:
            print(f"Erro em on_start ao buscar donos: {e}")
            # Se falhar, usamos uma lista padrão
            self.owner_ids = [1, 2, 3, 4, 5] 

    # ----- Mix de Testes  -----

    # Tarefa com peso 4 (40%) 
    @task(4)
    def get_all_owners(self):
        self.client.get("/api/customer/owners", name="GET /owners")

    # Tarefa com peso 3 (30%) [cite: 17]
    @task(3)
    def get_owner_by_id(self):
        if not self.owner_ids:
            return # Pula esta tarefa se não tivermos IDs

        # Escolhe um ID aleatório da lista que pegamos no on_start
        owner_id = random.choice(self.owner_ids)
        
        self.client.get(f"/api/customer/owners/{owner_id}", name="GET /owners/{id}")

    # Tarefa com peso 2 (20%) 
    @task(2)
    def get_vets(self):
        self.client.get("/api/vet/vets", name="GET /vets")

    # Tarefa com peso 1 (10%) [cite: 19]
    @task(1)
    def create_owner(self):
        # Dados simples para o cadastro [cite: 19]
        new_owner_data = {
            "firstName": "Locust",
            "lastName": f"User_{random.randint(1, 10000)}",
            "address": "123 Test Street",
            "city": "Testville",
            "telephone": f"555{random.randint(1000, 9999)}"
        }
        
        self.client.post("/api/customer/owners", json=new_owner_data, name="POST /owners")