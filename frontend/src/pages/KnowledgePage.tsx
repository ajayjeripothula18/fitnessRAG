import React, { useState } from 'react';
import { ingestionService } from '../services/ingestionService';
import { Loader2, CheckCircle, AlertTriangle } from 'lucide-react';

const KnowledgePage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);
  const [chunksIngested, setChunksIngested] = useState<number | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    // Clear previous status when new file is selected
    setUploadError(null);
    setUploadSuccess(null);
    setChunksIngested(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadError('Please select a file first');
      return;
    }

    setIsUploading(true);
    setUploadError(null);
    setUploadSuccess(null);
    setChunksIngested(null);

    try {
      const response = await ingestionService.uploadFile(file);
      setUploadSuccess('File uploaded successfully');
      setChunksIngested(response.chunks_ingested ?? null);
      // Clear file input after successful upload
      setFile(null);
    } catch (error: any) {
      let errorMessage = 'An unknown error occurred';

      if (error.response) {
        const status = error.response.status;
        if (status === 401) {
          errorMessage = 'Unauthorized access';
        } else if (status === 403) {
          errorMessage = 'Access forbidden - insufficient permissions';
        } else if (status === 413) {
          errorMessage = 'File size too large (maximum 5 MB)';
        } else if (status === 415) {
          errorMessage = error.response.data?.detail || 'Invalid file type or content';
        } else if (status === 503) {
          errorMessage = 'Service temporarily unavailable';
        } else {
          errorMessage = error.response.data?.detail || 'Server error occurred';
        }
      } else if (error.request) {
        errorMessage = 'Network error - please check your connection';
      }

      setUploadError(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const acceptedExtensions = ['.txt', '.md', '.csv'];

  return (
    <div className="knowledge-page p-6">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <div>
            <h3 className="text-lg font-semibold mb-4">Knowledge Base Upload</h3>
            <p className="mb-4">
              Upload fitness-related documents to expand the AI Coach's knowledge base.
            </p>

            <div className="space-y-4">
              <div>
                <label htmlFor="file-input" className="block mb-2 text-sm font-medium text-muted-foreground">
                  Select File
                </label>
                <input
                  id="file-input"
                  type="file"
                  accept={acceptedExtensions.map(ext => ext.substring(1)).join(',')}
                  className="block w-full text-sm text-muted-foreground cursor-pointer"
                  onChange={handleFileChange}
                  disabled={isUploading}
                />
                {file && (
                  <p className="mt-2 text-sm text-muted-foreground">
                    {file.name} ({Math.round(file.size / 1024)} KB)
                  </p>
                )}
                <p className="text-xs text-muted-foreground">
                  Supported file types: .txt, .md, .csv<br />
                  Maximum file size: 5 MB
                </p>
              </div>

              <button
                onClick={handleUpload}
                disabled={isUploading || !file}
                className="w-full flex items-center justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <CheckCircle className="mr-2 h-4 w-4" />
                    Upload File
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {(uploadError || uploadSuccess) && (
          <div className="mb-6">
            {uploadError && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <AlertTriangle className="h-5 w-5 text-red-400" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Upload Error</h3>
                    <div className="mt-2 text-sm text-red-700">{uploadError}</div>
                  </div>
                </div>
              </div>
            )}
            {uploadSuccess && (
              <div className="rounded-md bg-blue-50 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <CheckCircle className="h-5 w-5 text-blue-400" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-blue-800">Success</h3>
                    <div className="mt-2 text-sm text-blue-700">
                      {uploadSuccess}
                      {chunksIngested !== null && (
                        <>
                          <br />
                          {chunksIngested} text chunks created
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        <div>
          <div>
            <h3 className="text-lg font-semibold mb-4">How It Works</h3>
            <ol className="list-decimal pl-5 space-y-2">
              <li>Select a .txt, .md, or .csv file (max 5 MB)</li>
              <li>The file is validated for type, size, and content</li>
              <li>Content is processed into searchable text chunks</li>
              <li>Chunks are stored and made available to the AI Coach</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgePage;