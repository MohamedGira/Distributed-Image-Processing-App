// src/ImageUploadForm.js
import { useForm } from "react-hook-form";
import axios from "axios";
import { populateImagesFormData } from "./helpers";
import { toast } from "react-toastify";
import React from "react";
const options = [
  { label: "Grayscale", value: "grayscale" },
  { label: "Edge Detection", value: "edge_detection" },
  { label: "Thresholding", value: "thresholding" },
  { label: "Inversion", value: "inversion" },
  { label: "Blurring", value: "blurring" },
  { label: "Sharpening", value: "sharpening" },
  { label: "Smoothing", value: "smoothing" },
  { label: "Dilation", value: "dilation" },
  { label: "Erosion", value: "erosion" },
  { label: "Convert RGB", value: "convert_RGB" },
];
const ImageUploadForm = ({
  taskIds,
  setTaskIds,
}: {
  taskIds: string[];
  setTaskIds: any;
}) => {
  type FormInputs = {
    process: string;
    images: File[];
  };
  const { register, handleSubmit, watch } = useForm<FormInputs>();

  const onSubmit = async (data: any) => {
    try {
      const formData = populateImagesFormData(data);
      formData.append("process", data.process);
      console.log(
        data.images,
        formData.get("images"),
        typeof formData.get("images")
      );
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_HOST}:${process.env.REACT_APP_BACKEND_PORT}/upload`,
        formData
      );
      if (response.status === 200) {
        setTaskIds((old: any) => [...taskIds, "1"]);
        toast.success("Upload successful!");
      } else {
        toast.error("Upload failed!");
      }
    } catch (error) {
      console.error("Error uploading data:", error);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <fieldset>
          <legend>Image Processing App</legend>
          <div className="mb-3">
            <label className="form-label">Insert Images Here</label>
            <br />
            <input
              {...register("images")}
              type="file"
              multiple
              id="ImgInput"
              className="form-control-file"
            />
          </div>
          <div className="mb-3">
            <div>Select Image processing Operation</div>
            <select
              {...register("process")}
              className="form-select"
              aria-label="Default select example"
            >
              {options.map((el: any, index: number) => (
                <option key={index} value={el.value}>
                  {el.label}
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </fieldset>
        <br />
        <br />

        <div className="row row-cols-1 row-cols-md-2 g-4">
          <div className="col">
            <div className="card">
              {watch("images")?.length ? (
                <>
                  <div className="card-body">
                    <h5 className="card-title">Input Image</h5>
                  </div>
                  {Array.from(watch("images") ?? []).map((image: any, id) => (
                    <img
                      key={id}
                      src={URL.createObjectURL(image)}
                      className="card-img-top h-25 w-25 "
                      alt="..."
                    />
                  ))}
                </>
              ) : (
                <></>
              )}
            </div>
          </div>
          <div className="col">
            <div className="card">
              <h5 className="card-title">Processed Image</h5>
              <img src="..." className="card-img-top" alt="..." />
              <div className="card-body"></div>
            </div>
          </div>
        </div>
      </form>
    </>
  );
};

export default ImageUploadForm;
