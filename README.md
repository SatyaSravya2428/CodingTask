# CodingTask

Created API Gateway with different functionalities as shown in below picture

![42AB18B7-5960-48D7-9D3B-D28CEDE2FA6C_4_5005_c](https://github.com/SatyaSravya2428/CodingTask/assets/144446795/da9b8d9a-49a8-4821-b6a0-214092e0bf91)


1. Upload API:
   - Can access this API by URL https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1/upload
   - Upload the image in b64encode format
   - Need to add metadata information of this image in json format. 
   Example input data
    {
     "image" : b64encoded image file,
     "metdate": "This is a landscape picture of a river in Switzerland"
    }
   - This API uploads the image to Database in the backend

2. List All Images API:
   - Can access this API by URL https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1/allimages
   - User can filter the list of images by providing either of the two filters
      a. ImageID
      b. Date of the day image is uploaded
   - If neither of the filters are provided, the API returns entire list of images ids uploaded till date 

3. View Image API:
   - Can access this API by URL https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1/viewimage/{imageid}
   - It is mandatory to provide the imageid of the image that is required to view or download. example https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1/viewimage/12345
   

4. Delete Image API:
   - CCan access this API by URL https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1/deleteimage/{imageid}
   - Similar to View Image API, it is mandatory to provide the imageid of the image that is required to delete from the database. Example: https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1/deleteimage/12345

