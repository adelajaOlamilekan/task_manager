from fastapi import Header, HTTPException, status

def get_api_version(x_api_version:int= Header(...)):
  if x_api_version not in [1, 2]:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="API version not found"
    )
  return x_api_version