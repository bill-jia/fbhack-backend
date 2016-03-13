
var Friends = React.createClass({
  render: function(){
    return (
      <div>
        {
          data.map(function(item){
            return <Chip name={item.name} pic={item.image}/>
          })
        }
      </div>
    )
  }
});

var Chip = React.createClass({
  render: function(){
    return (
      <div className="chip">
        <img src={this.props.pic ? this.props.pic : '/static/default-profile.png'}/>
        <span>{this.props.name}</span>
      </div>
    )
  }
});

ReactDOM.render(
  <Friends />,
  document.getElementById('friends')
)
