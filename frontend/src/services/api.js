const API_BASE = import.meta.env.VITE_API_URL || '';

export const api = {
  getToken: () => localStorage.getItem('rebuild_token'),
  setToken: (token) => localStorage.setItem('rebuild_token', token),
  clearToken: () => localStorage.removeItem('rebuild_token'),

  async request(endpoint, options = {}) {
    const headers = { ...options.headers };
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    // If body is FormData, don't set Content-Type so browser sets boundary
    if (options.body && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(errorData.detail || 'An unexpected error occurred.');
    }

    return response.json();
  },

  // Auth
  login: (email, password) => api.request('/api/auth/login', { method: 'POST', body: { email, password } }),
  register: (userData) => api.request('/api/auth/register', { method: 'POST', body: userData }),
  getMe: () => api.request('/api/auth/me'),

  // ML & Vision
  predictMaterial: (formDataOrBase64) => {
    if (formDataOrBase64 instanceof FormData) {
      return api.request('/api/ml/predict-material', { method: 'POST', body: formDataOrBase64 });
    }
    const fd = new FormData();
    fd.append('base64_image', formDataOrBase64);
    return api.request('/api/ml/predict-material', { method: 'POST', body: fd });
  },

  assessQuality: (data) => api.request('/api/ml/assess-quality', { method: 'POST', body: data }),
  predictPrice: (data) => api.request('/api/ml/predict-price', { method: 'POST', body: data }),
  searchSimilar: (formDataOrBase64) => {
    if (formDataOrBase64 instanceof FormData) {
      return api.request('/api/ml/image-search', { method: 'POST', body: formDataOrBase64 });
    }
    const fd = new FormData();
    fd.append('base64_image', formDataOrBase64);
    return api.request('/api/ml/image-search', { method: 'POST', body: fd });
  },
  submitFeedback: (feedbackData) => api.request('/api/ml/feedback', { method: 'POST', body: feedbackData }),
  getModelMetrics: () => api.request('/api/ml/model-metrics'),

  // Listings
  getListings: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return api.request(`/api/listings${query ? `?${query}` : ''}`);
  },
  getListingDetail: (id) => api.request(`/api/listings/${id}`),
  createListing: (data) => api.request('/api/listings', { method: 'POST', body: data }),
  updateListing: (id, data) => api.request(`/api/listings/${id}`, { method: 'PUT', body: data }),
  deleteListing: (id) => api.request(`/api/listings/${id}`, { method: 'DELETE' }),
  toggleFavorite: (id) => api.request(`/api/listings/${id}/favorite`, { method: 'POST' }),
  getMyListings: () => api.request('/api/listings/my-listings'),
  getMyFavorites: () => api.request('/api/listings/my-favorites'),

  // Purchases & Negotiations
  createPurchaseRequest: (data) => api.request('/api/purchases/request', { method: 'POST', body: data }),
  getMyPurchaseRequests: () => api.request('/api/purchases/my-requests'),
  getIncomingRequests: () => api.request('/api/purchases/incoming-requests'),
  updatePurchaseRequest: (id, status) => api.request(`/api/purchases/request/${id}`, { method: 'PUT', body: { status } }),

  // Environmental Impact
  getEnvironmentalSummary: () => api.request('/api/environmental/summary'),
  calculateLCA: (material_name, quantity, unit) => api.request(`/api/environmental/calculate?material_name=${encodeURIComponent(material_name)}&quantity=${quantity}&unit=${encodeURIComponent(unit)}`),

  // Admin
  getAdminStats: () => api.request('/api/admin/statistics'),
  getAIMonitoring: () => api.request('/api/admin/ai-monitoring'),
  getAdminListings: () => api.request('/api/admin/listings'),
  flagListing: (id, status) => api.request(`/api/admin/flag-listing/${id}?new_status=${status}`, { method: 'POST' })
};
