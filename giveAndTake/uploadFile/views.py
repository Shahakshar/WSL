from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import File, TransferHistory
from .utils.cloudinary_utils import upload_to_cloudinary, delete_from_cloudinary
from django.db.models import Q


@api_view(['POST'])
def upload_file(request):
    file = request.FILES.get('file')
    name = request.data.get('name')
    owner = request.data.get('owner')
    original_owner = request.data.get('original_owner')

    if not file or not name or not owner or not original_owner:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    upload_response = upload_to_cloudinary(file)
    if 'error' in upload_response:
        return Response({'error': upload_response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    file_obj = File.objects.create(
        name=name,
        file_url=upload_response['url'],
        cloudinary_id=upload_response['public_id'],
        owner=owner,
        original_owner=original_owner
    )
    return Response({'public_id': file_obj.cloudinary_id, 'file_name': file_obj.name, 'file_url': file_obj.file_url}, status=status.HTTP_201_CREATED)

# @api_view(['DELETE'])
# def delete_file(request, file_id):
#     user_email = request.data.get('email')  # Assume user identity is passed
#     if not user_email:
#         return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         file_obj = File.objects.get(id=file_id)
#     except File.DoesNotExist:
#         return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     if file_obj.original_owner.lower() != user_email.lower():
#         return Response({'error': 'You are not authorized to delete this file'}, status=status.HTTP_403_FORBIDDEN)

#     delete_response = delete_from_cloudinary(file_obj.cloudinary_id)
#     if 'error' in delete_response:
#         return Response({'error': delete_response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     file_obj.delete()
#     return Response({'message': 'File deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def transfer_file(request):
    public_id = request.data.get('uplic_id')
    from_user = request.data.get('from_user')
    to_user = request.data.get('to_user')

    if not public_id or not to_user:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    # check if user exists whom u want to transfer the file very important thing before transfer 
    # this for security reasons

    file_obj = File.objects.filter(cloudinary_id=public_id).first()
    if not file_obj:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


    # Update the owner of the file

    if file_obj.owner != from_user:
        return Response({'error': 'You have not authorize for transfer'}, status=status.HTTP_400_BAD_REQUEST)
    previous_owner = file_obj.owner
    file_obj.owner = to_user
    file_obj.save()

    # Log the transfer history (not implemented here, but you can add it)
    TransferHistory.objects.create(
        file_name=file_obj.name,
        from_user=previous_owner,
        to_user=to_user,
        action='TRANSFER'
    )
    
    return Response({'message': 'File transferred successfully', 'new_owner': file_obj.owner}, status=status.HTTP_200_OK)

@api_view(['POST'])
def revoke_transfer(request):
    public_id = request.data.get('public_id')
    original_owner = request.data.get('original_owner')

    if not public_id or not original_owner:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        file_obj = File.objects.get(cloudinary_id=public_id)
    except File.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    # Revoke the transfer by setting the owner back to the original owner
    if file_obj.original_owner != original_owner:
        return Response({'error': 'Original owner does not match'}, status=status.HTTP_400_BAD_REQUEST)
    file_obj.owner = original_owner
    file_obj.save()

    # Log the transfer history for revocation
    TransferHistory.objects.create(
        file_name=file_obj.name,
        from_user=file_obj.owner,
        to_user=original_owner,
        action='REVOKE'
    )
    return Response({'message': 'Transfer revoked successfully', 'owner': file_obj.owner}, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_file(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Case-insensitive query
    files = File.objects.filter(
        Q(owner__iexact=email) | Q(original_owner__iexact=email)
    )

    if not files.exists():
        return Response({'error': 'No accessible files found'}, status=status.HTTP_404_NOT_FOUND)

    result = []
    for file_obj in files:
        result.append({
            'name': file_obj.name,
            'file_url': file_obj.file_url,
            'created_at': file_obj.created_at,
            'public_id': file_obj.cloudinary_id,
        })

    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_history(request):
    history = TransferHistory.objects.all().order_by('-transferred_at')
    result = []
    for record in history:
        result.append({
            'file_name': record.file_name,
            'from_user': record.from_user,
            'to_user': record.to_user,
            'action': record.action,
            'transferred_at': record.transferred_at,
        })  
    return Response(result, status=status.HTTP_200_OK)
