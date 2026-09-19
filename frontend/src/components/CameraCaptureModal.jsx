import React, { useState, useRef, useEffect } from 'react';
import { Camera, RefreshCw, Check, X, AlertCircle, SwitchCamera } from 'lucide-react';

/**
 * Real Device Camera Capture Modal
 * Supports front/rear facingMode, video preview, canvas snapshot, retake, and robust error handling.
 */
export default function CameraCaptureModal({ isOpen, onClose, onPhotoCaptured }) {
  const [stream, setStream] = useState(null);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // Default to rear camera on mobile
  const [isLoading, setIsLoading] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Initialize or reconfigure camera stream when modal opens or facingMode changes
  useEffect(() => {
    if (isOpen && !capturedPhoto) {
      startCamera();
    } else {
      stopCamera();
    }
    return () => {
      stopCamera();
    };
  }, [isOpen, facingMode]);

  const startCamera = async () => {
    stopCamera();
    setErrorMsg(null);
    setIsLoading(true);

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setErrorMsg("Camera access is not supported by your browser or environment. Please use file upload instead.");
      setIsLoading(false);
      return;
    }

    try {
      const constraints = {
        video: {
          facingMode: { ideal: facingMode },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      };

      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error("Camera access error:", err);
      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
        setErrorMsg("Camera permission was denied. Please allow camera permissions in your browser settings, or choose 'Upload Image'.");
      } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
        setErrorMsg("No camera device was detected on your device. Please connect a camera or use 'Upload Image'.");
      } else if (err.name === "NotReadableError" || err.name === "TrackStartError") {
        setErrorMsg("Camera is already in use by another application. Please close other camera apps and retry.");
      } else if (window.location.protocol !== "https:" && window.location.hostname !== "localhost") {
        setErrorMsg("Camera access requires a secure connection (HTTPS) or localhost.");
      } else {
        setErrorMsg(`Unable to access camera: ${err.message || "Unknown error"}. You can upload an image file instead.`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const handleCapture = () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
    setCapturedPhoto(dataUrl);
    stopCamera();
  };

  const handleRetake = () => {
    setCapturedPhoto(null);
    startCamera();
  };

  const handleUsePhoto = () => {
    if (capturedPhoto) {
      onPhotoCaptured(capturedPhoto);
      handleClose();
    }
  };

  const handleToggleFacingMode = () => {
    setFacingMode(prev => (prev === 'environment' ? 'user' : 'environment'));
  };

  const handleClose = () => {
    stopCamera();
    setCapturedPhoto(null);
    setErrorMsg(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-lg rounded-2xl bg-white shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <div className="flex items-center gap-2 text-emerald-800 font-semibold text-lg">
            <Camera className="w-5 h-5 text-emerald-600" />
            <span>Capture Material Photo</span>
          </div>
          <button
            onClick={handleClose}
            className="p-1 rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Viewfinder Area */}
        <div className="relative bg-black flex items-center justify-center min-h-[320px] max-h-[440px] overflow-hidden">
          {errorMsg ? (
            <div className="p-6 text-center text-red-200 flex flex-col items-center gap-3">
              <AlertCircle className="w-12 h-12 text-red-400" />
              <p className="text-sm font-medium text-white">{errorMsg}</p>
              <button
                onClick={startCamera}
                className="mt-2 inline-flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-xs font-semibold transition"
              >
                <RefreshCw className="w-4 h-4" />
                Retry Camera
              </button>
            </div>
          ) : capturedPhoto ? (
            <img src={capturedPhoto} alt="Captured Material" className="w-full h-auto max-h-[440px] object-contain" />
          ) : (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-auto max-h-[440px] object-contain"
                onLoadedMetadata={() => setIsLoading(false)}
              />
              {/* Viewfinder Target Grid Overlay */}
              <div className="absolute inset-8 border-2 border-dashed border-white/40 rounded-xl pointer-events-none flex items-center justify-center">
                <span className="text-white/70 text-xs bg-black/40 px-3 py-1 rounded-full backdrop-blur-sm">
                  Center material in frame
                </span>
              </div>

              {/* Camera Switch button (Mobile front/rear) */}
              <button
                type="button"
                onClick={handleToggleFacingMode}
                title="Switch Camera (Front/Rear)"
                className="absolute top-4 right-4 p-2.5 bg-black/50 hover:bg-black/70 text-white rounded-full backdrop-blur-sm transition"
              >
                <SwitchCamera className="w-5 h-5" />
              </button>
            </>
          )}

          {isLoading && !errorMsg && (
            <div className="absolute inset-0 bg-black/60 flex items-center justify-center text-white text-sm">
              <RefreshCw className="w-6 h-6 animate-spin mr-2" />
              Starting camera...
            </div>
          )}

          {/* Hidden Canvas used for high-res photo capture */}
          <canvas ref={canvasRef} className="hidden" />
        </div>

        {/* Action Controls */}
        <div className="px-6 py-4 bg-gray-50 flex items-center justify-between">
          {capturedPhoto ? (
            <>
              <button
                type="button"
                onClick={handleRetake}
                className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 bg-white hover:bg-gray-100 rounded-xl text-sm font-medium transition"
              >
                <RefreshCw className="w-4 h-4" />
                Retake
              </button>
              <button
                type="button"
                onClick={handleUsePhoto}
                className="inline-flex items-center gap-2 px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm font-semibold shadow-md shadow-emerald-600/20 transition"
              >
                <Check className="w-4 h-4" />
                Use Photo
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                onClick={handleClose}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 text-sm font-medium transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleCapture}
                disabled={isLoading || !!errorMsg}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl text-sm font-semibold shadow-md shadow-emerald-600/20 transition"
              >
                <Camera className="w-4 h-4" />
                Capture Photo
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
