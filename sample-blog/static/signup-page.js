App.controller('signupCtrl', ['$scope', function($scope) {

    $scope.signup = function() {
        const params = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                username: $scope.username,
                displayname: $scope.displayname,
                email: $scope.email,
                pswrd: $scope.pswrd,
            })
        };
        fetch(`/sign_up`, params)
            .then(resp => resp.json())
            .then(json => {
                console.log(json);
                if (json.error) {
                    return;
                }
                window.location.href = '/';
            })
    }

}])