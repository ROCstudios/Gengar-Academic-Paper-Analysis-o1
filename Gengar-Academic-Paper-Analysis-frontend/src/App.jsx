import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

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
      const response = await fetch('https://devai2.nobleblocks.com/api/pdf/upload', {
      // const response = await fetch('http://127.0.0.1:5000/pdf/upload', {
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

      let cleanedResponse;
      try {
        const rawResponse = await response.text();
        cleanedResponse = rawResponse.slice(1, -1);
        console.log('Upload successful:', rawResponse)
        setAnalysisResults(rawResponse)
      } catch (error) {
        console.error('Error parsing response:', error);
        cleanedResponse = {
          error: 'Failed to parse server response',
          details: error.message
        };
      }
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
            <ReactMarkdown>
              {typeof analysisResults === 'string' 
                ? analysisResults.slice(1, -1).replaceAll('****', '**\n**').replaceAll('-', '\n-').replaceAll('----', '\n\n\n\n').replaceAll('-### ', '### ').replaceAll('1. ', '\n1. ').replaceAll('2. ', '\n2. ').replaceAll('3. ', '\n3. ').replaceAll('4. ', '\n4. ').replaceAll('5. ', '\n5. ').replaceAll('-#### ', '#### ')
                : JSON.stringify(analysisResults, null, 2)}
            </ReactMarkdown>
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
