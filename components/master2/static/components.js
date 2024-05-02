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
const CardItem = (count, alt) => {
  return `    <style>
  .resp{
    display:flex;
    flex-direction:row;
    align-items:center;
  }
  @media (max-width: 768px) {
      /* For small screens */
      .w-50 {
          width: 100% !important; /* Set width of table cells to 100% */
      }
      .img-fluid {
          width: 100% !important; /* Set image width to 100% */
          display: block; /* Ensure images are centered */
          margin: auto; /* Center images horizontally */
      }
      .resp{
        display:block;
      }
  }
</style>

<div style="width: 100%;">
  <div class="resp">
      <div class="w-50">
          <div class="card mb-3">
              <div class="card-body">
                  <h5 class="text-center align-center">&nbsp;</h5>
                  <img class="img-fluid" id="${count}_input" alt="${alt}">
              </div>
          </div>
      </div>
      <div class="w-50">
          <div class="card mb-3">
              <div class="card-body" id="${count}_parent">
                  
              </div>
          </div>
      </div>
  </div>
</div>
            `;
};

const ImageUploadForm = () => {
  return `
      <form class="m-5" onSubmit="submitForm(event)">
        <fieldset>
          <legend>Image Processing App</legend>
          <div class="mb-3">
            <label class="form-label">Insert Images Here</label>
            <br />
            <input name="images" type="file" multiple id="ImgInput" class="form-control-file" />
          </div>
          <div class="mb-3">
            <div>Select Image processing Operation</div>
            <select name="process" class="form-select" aria-label="Default select example">
              ${options
                .map(
                  (option) =>
                    `<option value="${option.value}">${option.label}</option>`
                )
                .join("")}
            </select>
          </div>

          <button type="submit" class="btn btn-primary">Submit</button>
        </fieldset>
        <br />
        <br />

          <div class="col">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Input Image</h5>
                <ul id="inputImage" class="list-group list-group-flush"></ul>
              </div>
            </div>
          </div>
      </form>
    `;
};

const OutputContainer = (id) => {
  return `
  <div id="${id}_parent">
  <div id="${id}_status"></div>
  </div>
  `;
};
