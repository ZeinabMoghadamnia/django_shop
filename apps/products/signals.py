from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Image, Product


@receiver(post_save, sender=Product)
def calculate_discounted_price(sender, instance, **kwargs):
    if instance.discount is None and instance.category.discount is None and instance.brand.discount is None:
        instance.discounted_price = None
    else:
        discounts = []
        if hasattr(instance, 'discount') and instance.discount:
            if instance.discount.discount_type == 'percentage':
                instance.discounted_price = instance.price - ((instance.discount.value / 100) * instance.price)
            elif instance.discount.discount_type == 'amount':
                instance.discounted_price = instance.price - int(instance.discount.value)
            discounts.append(instance.discounted_price)

        if hasattr(instance, 'category') and instance.category and instance.category.discount:
            if instance.category.discount.discount_type in ['percentage', 'amount']:
                if instance.category.discount.discount_type == 'percentage':
                    instance.discounted_price = instance.price - ((instance.category.discount.value / 100) * instance.price)
                elif instance.category.discount.discount_type == 'amount':
                    instance.discounted_price = instance.price - int(instance.category.discount.value)
                discounts.append(instance.discounted_price)

            if instance.category.parent and instance.category.parent.discount and instance.category.parent.discount.discount_type in [
                'percentage', 'amount']:
                if instance.category.parent.discount.discount_type == 'percentage':
                    instance.discounted_price = instance.price - ((instance.category.parent.discount.value / 100) * instance.price)
                elif instance.category.parent.discount.discount_type == 'amount':
                    instance.discounted_price = instance.price - int(instance.category.parent.discount.value)
                discounts.append(instance.discounted_price)

        if instance.brand.discount and instance.brand.discount.discount_type in ['percentage', 'amount']:
            if instance.brand.discount.discount_type == 'percentage':
                instance.discounted_price = instance.price - ((instance.brand.discount.value / 100) * instance.price)
            elif instance.brand.discount.discount_type == 'amount':
                instance.discounted_price = instance.price - int(instance.brand.discount.value)
            discounts.append(instance.discounted_price)

        instance.discounted_price = min(discounts)

    post_save.disconnect(calculate_discounted_price, sender=Product)
    instance.save()
    post_save.connect(calculate_discounted_price, sender=Product)


@receiver(pre_save, sender=Image)
def validate_main_image(sender, instance, **kwargs):
    if instance.is_main:
        existing_main_image = Image.objects.filter(product=instance.product, is_main=True).exclude(id=instance.id)

        if existing_main_image.exists():
            raise ValidationError('لطفاً یک عکس را به عنوان عکس اصلی انتخاب کنید!')

        other_images = Image.objects.filter(product=instance.product).exclude(id=instance.id)
        other_images.update(is_main=False)

    else:
        main_image_exists = Image.objects.filter(product=instance.product, is_main=True).exclude(
            id=instance.id).exists()

        if not main_image_exists:
            raise ValidationError('لطفاً یک عکس را به عنوان عکس اصلی انتخاب کنید!')