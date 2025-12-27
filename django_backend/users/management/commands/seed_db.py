from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Tag, Brand, Product, ProductImage
from orders.models import ShippingAddress
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create users
        self.stdout.write('Creating users...')
        
        # Admin user
        admin, created = User.objects.get_or_create(
            email='admin@ecommerce.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin.email}'))
        
        # Seller user
        seller, created = User.objects.get_or_create(
            email='seller@ecommerce.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Seller',
                'role': 'seller',
                'is_active': True,
            }
        )
        if created:
            seller.set_password('seller123')
            seller.save()
            self.stdout.write(self.style.SUCCESS(f'Created seller user: {seller.email}'))
        
        # Customer user
        customer, created = User.objects.get_or_create(
            email='customer@ecommerce.com',
            defaults={
                'first_name': 'Jane',
                'last_name': 'Customer',
                'role': 'customer',
                'is_active': True,
            }
        )
        if created:
            customer.set_password('customer123')
            customer.save()
            self.stdout.write(self.style.SUCCESS(f'Created customer user: {customer.email}'))
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            ('Electronics', 'Electronic devices and accessories'),
            ('Clothing', 'Apparel and fashion items'),
            ('Books', 'Books and educational materials'),
            ('Home & Garden', 'Home improvement and garden supplies'),
            ('Sports', 'Sports equipment and accessories'),
        ]
        
        categories = {}
        for name, desc in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories[name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
        
        # Create tags
        self.stdout.write('Creating tags...')
        tags_data = ['New', 'Sale', 'Popular', 'Trending', 'Best Seller']
        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag_name}'))
        
        # Create brands
        self.stdout.write('Creating brands...')
        brands_data = ['Apple', 'Samsung', 'Nike', 'Adidas', 'Sony']
        brands = {}
        for brand_name in brands_data:
            brand, created = Brand.objects.get_or_create(name=brand_name)
            brands[brand_name] = brand
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created brand: {brand_name}'))
        
        # Create products
        self.stdout.write('Creating products...')
        products_data = [
            {
                'title': 'iPhone 15 Pro',
                'description': 'Latest iPhone with advanced features and powerful performance',
                'price': Decimal('999.99'),
                'stock_quantity': 50,
                'category': categories['Electronics'],
                'brand': brands['Apple'],
                'discount': Decimal('0'),
                'is_featured': True,
            },
            {
                'title': 'Samsung Galaxy S24',
                'description': 'Flagship Android smartphone with stunning display',
                'price': Decimal('899.99'),
                'stock_quantity': 45,
                'category': categories['Electronics'],
                'brand': brands['Samsung'],
                'discount': Decimal('10'),
                'is_featured': True,
            },
            {
                'title': 'Nike Air Max 90',
                'description': 'Classic running shoes with air cushioning technology',
                'price': Decimal('129.99'),
                'stock_quantity': 100,
                'category': categories['Sports'],
                'brand': brands['Nike'],
                'discount': Decimal('15'),
                'is_featured': False,
            },
            {
                'title': 'Adidas Ultraboost',
                'description': 'Premium running shoes with boost cushioning',
                'price': Decimal('180.00'),
                'stock_quantity': 75,
                'category': categories['Sports'],
                'brand': brands['Adidas'],
                'discount': Decimal('0'),
                'is_featured': False,
            },
            {
                'title': 'Sony WH-1000XM5',
                'description': 'Industry-leading noise canceling headphones',
                'price': Decimal('399.99'),
                'stock_quantity': 30,
                'category': categories['Electronics'],
                'brand': brands['Sony'],
                'discount': Decimal('20'),
                'is_featured': True,
            },
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults={
                    **product_data,
                    'seller': seller,
                }
            )
            if created:
                # Add tags
                product.tags.add(tags['New'], tags['Popular'])
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.title}'))
        
        # Create shipping address for customer
        self.stdout.write('Creating shipping address...')
        address, created = ShippingAddress.objects.get_or_create(
            user=customer,
            full_name='Jane Customer',
            defaults={
                'phone_number': '+1234567890',
                'address_line1': '123 Main Street',
                'city': 'New York',
                'postal_code': '10001',
                'country': 'USA',
                'is_default': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created shipping address'))
        
        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('\nTest accounts:')
        self.stdout.write(f'  Admin: admin@ecommerce.com / admin123')
        self.stdout.write(f'  Seller: seller@ecommerce.com / seller123')
        self.stdout.write(f'  Customer: customer@ecommerce.com / customer123')
