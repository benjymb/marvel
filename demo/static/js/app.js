/**
 * Created by benjy on 6/29/17.
 */
angular.element(document).ready(function () {
    componentHandler.upgradeAllRegistered();
});

angular.module('demoApp', [])
    .config(['$interpolateProvider',
        function ($interpolateProvider) {
            $interpolateProvider.startSymbol('[[').endSymbol(']]');
        }
    ])
    .controller('MainAppController', ['$scope', '$http', function ($scope, $http) {
        $scope.currentAction = '';
        $scope.searchMode = false;
        $scope.selectedIndex = 0;
        $scope.buttonMode = 'search';
        $scope.dataUrl = '';
        $scope.characterId = null;

        function cleanScopeData() {
            $scope.recentCharacters = null;
            $scope.searchResults = null;
        }

        $scope.changeIndex = function (newValue, url) {
            cleanScopeData();
            $scope.selectedIndex = newValue;
            $scope.dataUrl = url;
            $scope.getData();

        };
        $scope.changeMode = function(url){
            if (!$scope.searchMode) {
                $scope.dataUrl = url + '?query=' + prompt("Ingrese un nombre para buscar");
                $scope.searchMode = true;
                $scope.selectedIndex = 2;
                $scope.buttonMode = 'close';
                $scope.getData();
            } else {
                $scope.searchMode = false;
                $scope.selectedIndex = 0;
                $scope.buttonMode = 'search';
            }
        };
        $scope.getData = function(){
            $http.get($scope.dataUrl).then(function(response) {
                if ($scope.selectedIndex == "0"){
                    $scope.recentCharacters = response.data;
                } else if ($scope.selectedIndex == "2"){
                    console.log(response.data);
                    $scope.searchResults = response.data;
                }
            });
        };
    }]);

