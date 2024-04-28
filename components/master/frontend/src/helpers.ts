export const populateImagesFormData = (data: any) => {
  const formData = new FormData();
  for (const [key, value] of Object.entries(data)) {
    if (value instanceof File) {
      formData.append(key, value);
    } else if (value instanceof FileList) {
      Array.from(value).forEach((image: any) => formData.append(key, image));
    }
  }
  return formData;
};
