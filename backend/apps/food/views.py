from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, FoodItem
from .serializers import CategorySerializer, FoodItemSerializer, FoodItemListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category CRUD operations"""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class FoodItemViewSet(viewsets.ModelViewSet):
    """ViewSet for FoodItem CRUD operations"""
    
    queryset = FoodItem.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return FoodItemListSerializer
        return FoodItemSerializer

    def get_queryset(self):
        queryset = FoodItem.objects.select_related('category').all()
        
        # Filter by availability (default to available only)
        is_available = self.request.query_params.get('is_available', 'true')
        if is_available and is_available.lower() == 'true':
            queryset = queryset.filter(is_available=True)
        
        # Filter by category
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new food item (Admin only)"""
        if not request.user.is_admin:
            return Response({
                'success': False,
                'error': 'Only admins can create food items'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'success': True,
            'message': 'Food item created successfully',
            'data': FoodItemSerializer(serializer.instance).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update a food item (Admin only)"""
        if not request.user.is_admin:
            return Response({
                'success': False,
                'error': 'Only admins can update food items'
            }, status=status.HTTP_403_FORBIDDEN)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': 'Food item updated successfully',
            'data': FoodItemSerializer(serializer.instance).data
        })

    def destroy(self, request, *args, **kwargs):
        """Delete a food item (Admin only)"""
        if not request.user.is_admin:
            return Response({
                'success': False,
                'error': 'Only admins can delete food items'
            }, status=status.HTTP_403_FORBIDDEN)
        
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'success': True,
            'message': 'Food item deleted successfully'
        }, status=status.HTTP_200_OK)
