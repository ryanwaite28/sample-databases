const App = angular.module('sampleApp', []);

App.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('((');
	$interpolateProvider.endSymbol('))');
}]);

App.controller('sampleCtrl', ['$scope', function($scope){

  $scope.posts = [];
  $scope.min_post_id = null;
  $scope.is_loading = null;
  $scope.no_more_records = null;

  $scope.load_posts = function() {
    const post_ids = $scope.posts.map(post => post.id);
    $scope.min_post_id = post_ids.length ?
      Math.min(...post_ids) : null;

    const path = $scope.min_post_id ? `/get_latest_posts/${$scope.min_post_id}` : '/get_latest_posts';

    console.log(path);
    
    $scope.is_loading = true;
    fetch(path)
    .then(resp => resp.json())
    .then(json => {
      json.posts.forEach(post => {
        $scope.posts.push(post);
      });
      if (json.posts.length < 5) {
        $scope.no_more_records = true;
      }
      $scope.is_loading = false;
      $scope.$apply();
      console.log(json, $scope);
    })
  }

  $(document).ready(function(){
    $scope.load_posts();
  });

}])