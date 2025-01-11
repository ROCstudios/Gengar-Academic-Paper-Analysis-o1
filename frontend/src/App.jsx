import { useState } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [dragActive, setDragActive] = useState(false)

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
        throw new Error('Upload failed')
      }

      const data = await response.json()
      console.log('Upload successful:', data)
      
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
        <div className="h-full flex items-center justify-center">
          <div className="max-w-xl w-full">
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

            </div>
            {/* Upload Button */}
            <button
              className={`btn btn-primary mt-4 w-full ${!file || isUploading ? 'btn-disabled' : ''}`}
              onClick={handleUpload}
              disabled={!file || isUploading}
            >
              {isUploading ? 'Uploading...' : 'Upload File'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
