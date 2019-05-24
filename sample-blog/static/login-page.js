App.controller('loginCtrl', ['$scope', function($scope) {

    $scope.login = function() {
        console.log('logging in...');
        const params = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                email: $scope.e_or_u,
                pswrd: $scope.pswrd,
            })
        };
        fetch(`/log_in`, params)
            .then(resp => resp.json())
            .then(json => {
                console.log(json);
                if (json.error) {
                    return;
                }
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            })
    }

}])