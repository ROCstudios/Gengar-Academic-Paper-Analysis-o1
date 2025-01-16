import { useState } from 'react'
import AnalysisResults from './AnalysisResults'

function App() {
  const [file, setFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [dragActive, setDragActive] = useState(false)

  const [analysisResults, setAnalysisResults] = useState(null)
  const [error, setError] = useState(null)

  // Handle file selection
  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
    }
  }

  // Handle drag and drop
  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      setFile(droppedFile)
    }
  }

  // Handle file upload
  const handleUpload = async () => {
    if (!file) return

    try {
      setIsUploading(true)
      
      // Create FormData object
      const formData = new FormData()
      formData.append('file', file)

      // Upload file to server
      // const response = await fetch('https://devai2.nobleblocks.com/api/pdf/upload', {
      const response = await fetch('http://127.0.0.1:5000/pdf/upload', {
        method: 'POST',
        body: formData,
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          setUploadProgress(progress)
        },
      })

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || 'An unknown error occurred');
        return;
      } 


//       const olddata = `
// {
//     "calculation": {
//         "errors": []
//     },
//     "citation": {
//         "errors": [
//             {
//                 "errorCategory": "Citation/Reference Issues",
//                 "implications": "Invalidates citations as future works cannot be referenced, potentially undermining the credibility of the research.",
//                 "issue": "References include publications dated in the future (2025).",
//                 "recommendation": "Update references to include only published works or preprints with available information."
//             }
//         ]
//     },
//     "data_inconsistencies": {
//         "errors": []
//     },
//     "ethical": {
//         "errors": [
//             {
//                 "errorCategory": "Ethical Concerns",
//                 "implications": "Lack of transparency regarding potential biases or affiliations that may influence the research.",
//                 "issue": "Missing declaration of conflicts of interest.",
//                 "recommendation": "Include a clear conflict of interest statement detailing any affiliations or financial interests relevant to the research."
//             }
//         ]
//     },
//     "formatting": {
//         "errors": [
//             {
//                 "errorCategory": "Formatting Errors",
//                 "implications": "Reduces readability and compliance with standard journal formatting guidelines.",
//                 "issue": "Inconsistent formatting of figure captions and embedded figure descriptions within the text.",
//                 "recommendation": "Ensure that all figures and their captions are consistently formatted and properly placed according to journal guidelines."
//             }
//         ]
//     },
//     "logical": {
//         "errors": []
//     },
//     "methodical": {
//         "errors": [
//             {
//                 "errorCategory": "Methodological Errors",
//                 "implications": "Limits reproducibility and understanding of the methodology.",
//                 "issue": "Insufficient detail in the data synthesis process.",
//                 "recommendation": "Provide a more detailed description of the data synthesis modules and processes to enable reproducibility."
//             }
//         ]
//     },
//     "pdf_name": "/tmp/uploads/URSA-_Understanding_and_Verifying_Chain-of-thought_Reasoning_in_Multimodal_Mathematics.pdf",
//     "summary": {
//         "authors": "Ruilin Luo, Zhuofan Zheng, Yifan Wang, Yiyao Yu, Xinzhe Ni, Zicheng Lin, Jin Zeng, Yujiu Yang",
//         "calculationErrorCount": "0",
//         "citationErrorCount": "1",
//         "dataInconsistencyCount": "0",
//         "errorCount": "4",
//         "ethicalErrorCount": "1",
//         "formattingErrorCount": "1",
//         "logicalErrorCount": "0",
//         "methodicalErrorCount": "1",
//         "published": "8 Jan 2025",
//         "title": "URSA: Understanding and Verifying Chain-of-thought Reasoning in Multimodal Mathematics"
//     },
//     "timestamp": "2025-01-12T08:35:36.371711"
// }`;
//       const data = JSON.parse(olddata);
      let data;
      try {
        const rawResponse = await response.text();
        // Remove any non-JSON content before the first { and after the last }
        const cleanedResponse = rawResponse.substring(
          rawResponse.indexOf('{'), 
          rawResponse.lastIndexOf('}') + 1
        );
        data = JSON.parse(cleanedResponse);
      } catch (error) {
        console.error('Error parsing response:', error);
        data = {
          error: 'Failed to parse server response',
          details: error.message
        };
      }
      console.log('Upload successful:', data)
      setAnalysisResults(data)
      // Clear file after successful upload
      setFile(null)
      setUploadProgress(0)
      
    } catch (error) {
      console.error('Upload error:', error)
      // Handle error (show error message to user)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="w-full min-h-screen bg-base-200 flex"> {/* Add flex */}
      {/* Left Instructions Panel - 10% */}
      <div className="w-[20%] p-4 bg-base-100 shadow-lg flex flex-col justify-center items-center">
        <h2 className="text-lg font-bold mb-4">Instructions</h2>
        <h1 className="text-5xl font-bold text-center">Let's Check Your Paper!</h1>
        <p className="py-6 text-center">Just upload your paper and we'll check it for you!  We'll check for logical, methodological, and others for you.</p>
        <button className="btn btn-primary">Learn More</button>
      </div>

      {/* Right File Upload Area - 90% */}
      <div className="w-[80%] p-8">
          {error && (
            <div className="alert alert-error mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </div>
          )}
        <div className="h-full flex items-center justify-center">
          <div className="max-w-xl w-full">
          {analysisResults ? (
            <AnalysisResults data={analysisResults} />
          ) : (
          <div 
              className={`border-2 border-dashed rounded-lg p-12 text-center
                ${dragActive ? 'border-primary bg-base-200' : 'border-gray-300'}
                ${isUploading ? 'opacity-50' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {/* File Input */}
              <input 
                type="file" 
                className="file-input file-input-bordered w-full max-w-xs"
                onChange={handleFileSelect}
                disabled={isUploading}
              />

              <p className="mt-2 text-sm text-gray-500">
                or drag and drop your files here
              </p>

              {/* Selected File Info */}
              {file && (
                <div className="mt-4">
                  <p className="text-sm">Selected: {file.name}</p>
                  <p className="text-xs text-gray-500">
                    Size: {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              )}

              {/* Upload Progress */}
              {isUploading && (
                <progress 
                  className="progress progress-primary w-full mt-4" 
                  value={uploadProgress} 
                  max="100"
                ></progress>
              )}
              {/* Upload Button */}
              <button
                className={`btn btn-primary mt-4 w-full ${!file || isUploading ? 'btn-disabled' : ''}`}
                onClick={handleUpload}
                disabled={!file || isUploading}
              >
                {isUploading ? 'Uploading...' : 'Upload File'}
              </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
