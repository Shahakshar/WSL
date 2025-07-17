import cloudinary.uploader

def upload_to_cloudinary(file):
    try:
        response = cloudinary.uploader.upload(file, folder='giveAndTake')
        return {
            'url': response['secure_url'],
            'public_id': response['public_id']
        }
    except Exception as e:
        return {
            'error': str(e)
        }

def delete_from_cloudinary(public_id):
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        return {
            'error': str(e)
        }
