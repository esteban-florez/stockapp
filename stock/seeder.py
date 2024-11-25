from stock.models import Category, Movement, Product, Supplier, User

def seed():
  Movement.objects.all().delete()
  Product.objects.all().delete()
  Supplier.objects.all().delete()
  Category.objects.all().delete()
  User.objects.all().delete()
  
  tools = Category.objects.create(
    name='Herramientas',
    description='Herramientas para el trabajo y hogar.',
  )

  clothes = Category.objects.create(
    name='Ropa',
    description='Diferentes tipos de vestimenta.',
  )

  home_appliance = Category.objects.create(
    name='Electrodomésticos',
    description='Electrodomésticos fundamentales para el hogar.',
  )

  hammer = Product.objects.create(
    name='Martillo',
    description='Martillo con mango de madera y cabeza de hierro.',
    price=23.5,
    category=tools,
  )

  screw = Product.objects.create(
    name='Destornillador',
    description='Destornillador de estría magnético.',
    price=16.8,
    category=tools,
  )

  drill = Product.objects.create(
    name='Taladro',
    description='Taladro eléctrico para concreto y madera.',
    price=139.99,
    category=tools,
  )
  
  shirt = Product.objects.create(
    name='Franela',
    description='Franela marca Nike de color azul eléctrico.',
    price=49.25,
    category=clothes,
  )

  pants = Product.objects.create(
    name='Pantalón',
    description='Pantalón jean marca Levi\'s color azul claro.',
    price=30.56,
    category=clothes,
  )

  fridge = Product.objects.create(
    name='Nevera',
    description='Nevera marca Samsung del año 2020.',
    price=569.99,
    category=home_appliance,
  )
  
  supplier1 = Supplier.objects.create(
    name='TuEmpresa C.A.',
    description='Proveedores de herramientas de calidad.',
    category=tools,
  )

  supplier2 = Supplier.objects.create(
    name='MiCompañía C.A.',
    description='Empresa encargada de productos textiles.',
    category=clothes,
  )

  supplier3 = Supplier.objects.create(
    name='EmpresaInc C.A.',
    description='Empresa encargada de electrodomésticos.',
    category=home_appliance,
  )
  
  Movement.objects.create(
    amount=20,
    reason='Restock de martillos',
    product=hammer,
    supplier=supplier1,
  )

  Movement.objects.create(
    amount=10,
    reason='Compra de destornilladores',
    product=screw,
    supplier=supplier1,
  )

  Movement.objects.create(
    amount=5,
    reason='Compra de taladros',
    product=drill,
    supplier=supplier1,
  )
  
  Movement.objects.create(
    amount=-4,
    reason='Venta de destornilladores',
    product=screw,
  )

  Movement.objects.create(
    amount=50,
    product=shirt,
    supplier=supplier2,
  )
  
  Movement.objects.create(
    amount=50,
    product=pants,
    supplier=supplier2,
  )
  
  Movement.objects.create(
    amount=15,
    product=fridge,
    supplier=supplier3,
  )
  
  Movement.objects.create(
    amount=-10,
    reason='Venta de franelas',
    product=shirt,
  )
  
  Movement.objects.create(
    amount=-5,
    reason='Venta de neveras',
    product=fridge,
  )

  Movement.objects.create(
    amount=-5,
    product=pants,
  )

  User.objects.create_user(
    name='Luis Pérez',
    email='luis@ejemplo.com',
    password='pass1234',
  )
