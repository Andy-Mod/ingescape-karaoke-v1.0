import ingescape as igs
import base64

# Fonction pour envoyer un message au Whiteboard
def send_message(message):
    try:
        igs.service_call("Whiteboard", "chat", message, "")
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")


def add_Text(message,  x, y, color, token):
    try:
        arguments_list = (message,x,y,color)
        elementID = igs.service_call("Whiteboard", "addText", arguments_list, token)
        print(f"add Test: {arguments_list}")
        return elementID 
    except Exception as e:
        print(f"Failed to add Text: {e}")
"""   
def add_Image(Image,  x, y, widh, height):
    try:
        # Lire l'image et l'encoder en Base64
        #with open(Image, "rb") as img_file:
            #encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
        arguments_list = (Image, x, y, widh, height)
        elementID = igs.service_call("Whiteboard", "addImage", arguments_list, "")
        #print(f"add Image: {arguments_list}")
        print(f"add Image:")
        print (elementID)
        return elementID
    except Exception as e:
        print(f"Failed to add Image: {e}")"""
def add_image(image_url, x, y, width, height, token):
        """Ajoute une image sur le tableau blanc."""
        img_path =f"C:/Users/ghazo/Documents/Ingescape/sandbox/KaraokeIngescape/data/{image_url}"
        image_url = f"file:///{img_path}"
        arguments_list = (image_url, x, y, width, height)
        elementID = igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, token)
        igs.service_call("Whiteboard", "addImageFromUrl", (image_url, x, y, width, height), token)
def add_Image_From_URL(Image,  x, y ,token):
    try:
        img_path =f"C:/Users/ghazo/Documents/Ingescape/sandbox/KaraokeIngescape/data/{Image}"
        image_url = f"file:///{img_path}"
        arguments_list = (image_url, x, y)
        elementID = igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, token)
        print(f"add Image From URL: {arguments_list}")
        return elementID
    except Exception as e:
        print(f"Failed to add Image From UR: {e}")

def remove_Element (elemntID):
    try: 
        succeeded = igs.service_call("Whiteboard", "remove", elemntID, "")
        print(f"remove: {elemntID}")
        return succeeded
    except Exception as e:
        print(f"Failed to remove: {e}")

def hide_Labels ():
    try:
        igs.service_call("Whiteboard", "hideLabels",(),"")
        print("hide Labels")
    except Exception as e:
        print(f"Failed to hide labels: {e}")

def translate_element(elementId, dx, dy):
    try:
        arguments_list = (elementId, dx, dy)
        succ = igs.service_call("Whiteboard", "translate", arguments_list, "")
        print(f"translate: {arguments_list}")
        return succ 
    except Exception as e:
        print(f"Failed to add Text: {e}")

def clearWhitboard():
    try:
        igs.service_call("Whiteboard", "clear",(),"")
    except Exception as e:
        print(f"Failed to clear: {e}")

