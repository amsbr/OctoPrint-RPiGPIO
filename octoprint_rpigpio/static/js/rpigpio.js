$(function() {
    function RPiGPIOViewModel(parameters) {
        var self = this;

        self.onSettingsShown = function() {
            alert('teste');
            self.requestData();
        };

    }

    ADDITIONAL_VIEWMODELS.push([
        RPiGPIOViewModel,
        ["loginStateViewModel", "settingsViewModel"],
        []
    ]);

})
