# /shops/{client_pk}/products/{maildrop_pk}/reviews/{pk}/

# # /shops/shop_pk/products/product_pk/reviews/pk
# router = DefaultRouter()
# router.register(r'shops', ShopViewSet, basename='shops')
# ## generates:
# # /shops/
# # /shops/{pk}/

# shop_router = routers.NestedSimpleRouter(router, r'shops', lookup='shop')
# shop_router.register(r'products', MailDropViewSet, basename='products')
# ## generates:
# # /shops/{shop_pk}/products/
# # /shops/{shop_pk}/products/{maildrop_pk}/

# maildrops_router = routers.NestedSimpleRouter(shop_router, r'products', lookup='product')
# maildrops_router.register(r'reviews', MailRecipientViewSet, basename='reviews')
# ## generates:
# # /shops/{shop_pk}/products/{maildrop_pk}/reviews/
# # /shops/{shop_pk}/products/{maildrop_pk}/reviews/{pk}/
