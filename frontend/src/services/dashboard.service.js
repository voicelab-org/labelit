import ApiService from "@/services/api.service";

class DashboardService {
  constructor() {
    this.request = ApiService;
  }

  getStats(params = {}) {
    return this.request.get("/dashboard/", { params });
  }
}

export default new DashboardService();
