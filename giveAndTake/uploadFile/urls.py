from django.urls import path
from uploadFile.views import upload_file, transfer_file, revoke_transfer, get_file, get_all_history

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    # path('delete/<int:file_id>/', delete_file, name='delete_file'),

    path('transfer/', transfer_file, name='transfer_file'), 
    path('revoke/', revoke_transfer, name='revoke_transfer'),
    path('accessfile/', get_file, name='get_file'),

    path('history/', get_all_history, name='get_all_history'), # just for testing purposes and also given in doc so i thought to put this endpoint
]