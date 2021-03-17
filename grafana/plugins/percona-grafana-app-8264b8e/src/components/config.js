
export class PerconaAppConfigCtrl {
  constructor() {
    this.appEditCtrl.setPostUpdateHook(this.postUpdate.bind(this));
  }

  postUpdate() {
    if (!this.appModel.enabled) {
      return Promise.resolve();
    }

    return this.appEditCtrl.importDashboards().then(() => {
      return {
        url: "/dashboard/db/summary-dashboard",
        message: "Percona app installed!"
      };
    });
  }
}

PerconaAppConfigCtrl.templateUrl = 'components/config.html';
