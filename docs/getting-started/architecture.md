# Documentação da Arquitetura

## Visão Geral da Clean Architecture

Este documento detalha a implementação da Clean Architecture neste projeto, explicando as decisões de design e como cada camada interage com as outras.

## Princípios Fundamentais

### 1. Regra de Dependência

As dependências sempre apontam para dentro, em direção ao domínio:

```
Presentation → Application → Domain
Infrastructure → Domain
```

- **Domain**: Não depende de nada
- **Application**: Depende apenas do Domain
- **Infrastructure**: Depende do Domain (através de interfaces)
- **Presentation**: Depende de Application e Domain

### 2. Inversão de Dependência

As camadas externas dependem de abstrações (interfaces) definidas nas camadas internas:

```python
# Domain define a interface
class TenantRepository(ABC):
    @abstractmethod
    def save(self, tenant: Tenant) -> Tenant:
        pass

# Infrastructure implementa a interface
class DjangoTenantRepository(TenantRepository):
    def save(self, tenant: Tenant) -> Tenant:
        # Implementação específica do Django
        pass
```

## Detalhamento das Camadas

### Camada de Domínio (Domain)

**Responsabilidades:**
- Definir entidades de negócio
- Implementar regras de negócio
- Definir interfaces de repositório
- Definir exceções de domínio

**Características:**
- Não possui dependências externas
- Contém a lógica de negócio mais importante
- É a camada mais estável

#### Entidades

```python
class Entity(ABC):
    """Entidade base com propriedades universais"""
    
class Tenant(Entity):
    """Entidade rica com validações e comportamentos"""
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise DomainValidationError("Nome não pode ser vazio")
        self._name = value.strip()
        self._touch()
```

#### Repositórios (Interfaces)

```python
class TenantRepository(ABC):
    """Interface que define o contrato de persistência"""
    
    @abstractmethod
    def save(self, tenant: Tenant) -> Tenant:
        pass
    
    @abstractmethod
    def find_by_id(self, tenant_id: str) -> Optional[Tenant]:
        pass
```

### Camada de Aplicação (Application)

**Responsabilidades:**
- Orquestrar casos de uso
- Coordenar entidades e repositórios
- Definir DTOs para transferência de dados
- Tratar exceções de domínio

**Características:**
- Depende apenas do domínio
- Não contém lógica de negócio (delega para entidades)
- Define o fluxo de operações

#### Casos de Uso

```python
class TenantUseCases:
    def __init__(self, tenant_repository: TenantRepository):
        self._tenant_repository = tenant_repository
    
    def create_tenant(self, create_dto: CreateTenantDTO) -> TenantResponseDTO:
        # 1. Validar regras de negócio
        if self._tenant_repository.exists_by_slug(create_dto.slug):
            raise BusinessRuleViolationError("Slug já existe")
        
        # 2. Criar entidade (validações automáticas)
        tenant = Tenant(
            name=create_dto.name,
            slug=create_dto.slug,
            is_active=create_dto.is_active
        )
        
        # 3. Persistir
        saved_tenant = self._tenant_repository.save(tenant)
        
        # 4. Retornar DTO
        return TenantResponseDTO.from_entity(saved_tenant)
```

#### DTOs (Data Transfer Objects)

```python
@dataclass
class CreateTenantDTO:
    """DTO para entrada de dados"""
    name: str
    slug: str
    is_active: bool = True

@dataclass
class TenantResponseDTO:
    """DTO para saída de dados"""
    id: str
    name: str
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, tenant: Tenant):
        return cls(
            id=tenant.id,
            name=tenant.name,
            slug=tenant.slug,
            is_active=tenant.is_active,
            created_at=tenant.created_at,
            updated_at=tenant.updated_at
        )
```

### Camada de Infraestrutura (Infrastructure)

**Responsabilidades:**
- Implementar repositórios usando tecnologias específicas
- Mapear entidades para modelos de banco de dados
- Gerenciar persistência e transações

**Características:**
- Implementa interfaces definidas no domínio
- Contém detalhes técnicos específicos
- Pode ser substituída sem afetar outras camadas

#### Modelos Django

```python
class TenantModel(models.Model):
    """Modelo Django para persistência"""
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Repositórios Concretos

```python
class DjangoTenantRepository(TenantRepository):
    """Implementação usando Django ORM"""
    
    def save(self, tenant: Tenant) -> Tenant:
        try:
            model = TenantModel.objects.get(id=tenant.id)
            model = self._entity_to_model(tenant, model)
        except TenantModel.DoesNotExist:
            model = self._entity_to_model(tenant)
        
        model.save()
        return self._model_to_entity(model)
    
    def _entity_to_model(self, entity: Tenant, model: TenantModel = None) -> TenantModel:
        """Converte entidade para modelo Django"""
        if model is None:
            model = TenantModel()
        
        model.id = entity.id
        model.name = entity.name
        model.slug = entity.slug
        model.is_active = entity.is_active
        return model
    
    def _model_to_entity(self, model: TenantModel) -> Tenant:
        """Converte modelo Django para entidade"""
        return Tenant(
            name=model.name,
            slug=model.slug,
            is_active=model.is_active,
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
```

### Camada de Apresentação (Presentation)

**Responsabilidades:**
- Receber requisições HTTP
- Validar dados de entrada
- Chamar casos de uso apropriados
- Retornar respostas HTTP

**Características:**
- Atua como orquestradora de I/O
- Não contém lógica de negócio
- Converte entre formatos HTTP e DTOs

#### Views

```python
@api_view(['POST'])
def create_tenant(request):
    """View para criação de tenant"""
    try:
        # 1. Validar dados de entrada
        serializer = CreateTenantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # 2. Converter para DTO
        create_dto = serializer.to_dto()
        
        # 3. Executar caso de uso
        tenant_dto = tenant_use_cases.create_tenant(create_dto)
        
        # 4. Serializar resposta
        response_serializer = TenantResponseSerializer(tenant_dto.__dict__)
        return Response(response_serializer.data, status=201)
        
    except DomainValidationError as e:
        return Response({'error': str(e)}, status=400)
    except BusinessRuleViolationError as e:
        return Response({'error': str(e)}, status=409)
```

#### Serializers

```python
class CreateTenantSerializer(serializers.Serializer):
    """Serializer para validação de entrada"""
    name = serializers.CharField(max_length=255, min_length=2)
    slug = serializers.SlugField(max_length=100, min_length=2)
    is_active = serializers.BooleanField(default=True)
    
    def to_dto(self) -> CreateTenantDTO:
        return CreateTenantDTO(**self.validated_data)
```

## Fluxo de Dados

### Criação de Entidade

```
1. HTTP Request → View
2. View → Serializer (validação)
3. Serializer → DTO
4. View → Use Case (com DTO)
5. Use Case → Repository (interface)
6. Repository → Database
7. Database → Repository
8. Repository → Use Case (entidade)
9. Use Case → DTO
10. DTO → View
11. View → Serializer (resposta)
12. Serializer → HTTP Response
```

### Busca de Entidade

```
1. HTTP Request → View
2. View → Use Case (com parâmetros)
3. Use Case → Repository (interface)
4. Repository → Database
5. Database → Repository
6. Repository → Use Case (entidade ou None)
7. Use Case → DTO ou Exception
8. DTO → View
9. View → Serializer (resposta)
10. Serializer → HTTP Response
```

## Benefícios da Arquitetura

### 1. Testabilidade

Cada camada pode ser testada isoladamente:

```python
# Teste de entidade (sem dependências)
def test_tenant_validation():
    with pytest.raises(DomainValidationError):
        Tenant(name="", slug="test")

# Teste de caso de uso (com mocks)
def test_create_tenant_use_case():
    mock_repo = Mock()
    mock_repo.exists_by_slug.return_value = False
    
    use_case = TenantUseCases(mock_repo)
    result = use_case.create_tenant(create_dto)
    
    mock_repo.save.assert_called_once()
```

### 2. Flexibilidade

Fácil substituição de implementações:

```python
# Desenvolvimento: usar SQLite
dev_repository = DjangoTenantRepository()

# Produção: usar PostgreSQL
prod_repository = DjangoTenantRepository()

# Testes: usar mock
test_repository = MockTenantRepository()

# Casos de uso permanecem inalterados
use_cases = TenantUseCases(repository)
```

### 3. Manutenibilidade

Mudanças em uma camada não afetam outras:

- Mudança no banco de dados: apenas Infrastructure
- Mudança na API: apenas Presentation
- Mudança nas regras de negócio: apenas Domain

### 4. Escalabilidade

Fácil adição de novas funcionalidades:

```python
# Nova entidade
class Invoice(Document):
    pass

# Novo repositório
class InvoiceRepository(ABC):
    pass

# Novos casos de uso
class InvoiceUseCases:
    pass

# Novas views
def create_invoice(request):
    pass
```

## Padrões de Design Utilizados

### Repository Pattern

Abstrai a camada de persistência, permitindo trocar implementações sem afetar a lógica de negócio.

### DTO Pattern

Transfere dados entre camadas de forma segura, evitando vazamento de detalhes internos.

### Use Case Pattern

Encapsula operações de negócio específicas, mantendo a lógica organizada e testável.

### Entity Pattern

Encapsula dados e comportamentos relacionados, garantindo consistência e validação.

## Considerações de Performance

### 1. Lazy Loading

```python
# Evitar N+1 queries
def find_tenants_with_documents(self):
    return TenantModel.objects.prefetch_related('documents').all()
```

### 2. Caching

```python
# Cache em nível de repositório
def find_by_slug(self, slug: str) -> Optional[Tenant]:
    cache_key = f"tenant:slug:{slug}"
    cached = cache.get(cache_key)
    if cached:
        return self._model_to_entity(cached)
    
    model = TenantModel.objects.get(slug=slug)
    cache.set(cache_key, model, timeout=300)
    return self._model_to_entity(model)
```

### 3. Paginação

```python
# Paginação em casos de uso
def list_tenants(self, page: int = 1, size: int = 20) -> PaginatedTenantResponse:
    offset = (page - 1) * size
    tenants = self._repository.find_all(offset=offset, limit=size)
    total = self._repository.count_all()
    
    return PaginatedTenantResponse(
        items=[TenantResponseDTO.from_entity(t) for t in tenants],
        total=total,
        page=page,
        size=size
    )
```

## Conclusão

Esta implementação da Clean Architecture fornece uma base sólida para desenvolvimento de aplicações Django escaláveis e maintíveis, seguindo as melhores práticas de engenharia de software.

