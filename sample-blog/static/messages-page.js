App.controller('messagespageCtrl', ['$scope', '$vault', function($scope, $vault) {

    $scope.init = true;
    
    $scope.senders = [];
    $scope.sendersObj = {};
    $scope.messages = [];
    $scope.messagesObj = {};

    $scope.is_loading = null;
    $scope.no_more_records1 = null;
    $scope.no_more_records2 = null;

    $scope.you = null;
    $scope.currentSender = null;

    $scope.load_message_senders = function() {
        const ids_list = $scope.senders.map(msg => msg.id);
        const min_id = ids_list.length ? Math.min(...ids_list) : null;

        const path = min_id ? 
            `/users/${$scope.you.id}/get_message_senders/${min_id}` : 
            `/users/${$scope.you.id}/get_message_senders`;

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.senders.forEach(data => {
                    $scope.senders.push(data.sender);
                    $scope.sendersObj[data.sender.username] = data.sender;
                });
                if (json.senders.length < 5) {
                    $scope.no_more_records1 = true;
                }
                $scope.is_loading = false;
                $scope.$apply();
                console.log(json, $scope);
            });
    }

    $scope.load_messages = function() {
        $scope.messages = [];
        $scope.messagesObj = {};

        const sender_id = $scope.currentSender.id;
        const ids_list = $scope.messages.map(msg => msg.id);
        const min_id = ids_list.length ? Math.min(...ids_list) : null;

        const path = min_id ? 
            `/users/${$scope.you.id}/sender/${sender_id}/get_latest_messages/${min_id}` : 
            `/users/${$scope.you.id}/sender/${sender_id}/get_latest_messages`;

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.messages.forEach(message => {
                    $scope.messages.push(message);
                    $scope.messagesObj[message.uuid] = message;
                });
                if (json.messages.length < 5) {
                    $scope.no_more_records2 = true;
                }
                $scope.is_loading = false;
                $scope.$apply();
                console.log(json, $scope);
            });
    }

    $scope.setSender = function(sender) {
        $scope.currentSender = sender;
        $scope.load_messages();
    }

    $scope.clearSender = function() {
        $scope.currentSender = null;
    }

    $(document).ready(function() {
        $vault.check_session()
            .then(() => {
                $scope.you = $vault.you;
                $scope.load_message_senders()
                    .then(() => {
                        $scope.init = false;
                        $scope.$apply();
                    });
            });
    });

}])