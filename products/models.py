from django.db import models


class CatalogItem(models.Model):
    TYPE_CHOICES = [
        ('PRODUTO', 'produto'),
        ('SERVICO', 'serviço'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_stock_control(self):
        return self.type == 'PRODUTO'
      
    def clean(self):
        # Validação para garantir que produtos tenham estoque e serviços não tenham estoque
        from django.core.exceptions import ValidationError

        # Se for um produto, deve ter estoque definido
        if self.type == 'PRODUTO' and self.stock is None:
            raise ValidationError({'stock': 'Produto precisa de estoque.'})
        
        # Se for um serviço, não deve ter estoque definido
        if self.type == 'SERVICO' and self.stock is not None:
            raise ValidationError({
                'stock': 'Serviço não deve ter estoque.'
            })
    
    def save(self, *args, **kwargs):
        # Garantir que a validação seja chamada antes de salvar
        self.full_clean() # Chama o método de validação antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name