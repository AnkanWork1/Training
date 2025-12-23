"use client";

export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <>
      {/* Semi-transparent overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-30 z-40"
        onClick={onClose} // Clicking outside closes the modal
      ></div>

      {/* Modal card */}
      <div className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
        <div
          className="bg-white rounded-lg shadow-lg w-full max-w-md p-6 pointer-events-auto"
          onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
        >
          {/* Header */}
          <h2 className="text-2xl font-semibold mb-4">{title}</h2>

          {/* Content */}
          {children}

          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-3 right-3 text-gray-500 hover:text-gray-800"
          >
            ✕
          </button>
        </div>
      </div>
    </>
  );
}
