class ProcessController < ApplicationController
  def compute
    numbers = params[:numbers]
    if numbers.is_a?(Array) && numbers.all? { |n| n.is_a?(Numeric) }
      result = numbers.sum { |n| n * n }
      render json: { result: result }
    else
      render json: { error: "Invalid input. 'numbers' must be an array of numbers." }, status: :bad_request
    end
  end
end
